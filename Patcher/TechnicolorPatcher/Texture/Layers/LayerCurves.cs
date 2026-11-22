using SkiaSharp;
using TechnicolorPatcher.Types;
using TechnicolorPatcher.Util;
using YamlDotNet.Serialization;

namespace TechnicolorPatcher.Texture.Layers;

[YamlSerializable]
public class LayerCurves : LayerBase
{
    public static string LayerName => "curves";

    public List<Int2> Points { get; set; } = [];

    public void Validate()
    {
        int[] xVals = Points.Select(p => p.X).ToArray();
        if (!xVals.SequenceEqual(xVals.OrderBy(v => v)))
        {
            throw new ArgumentException("Curve points must be ordered by the x axis");
        }

        if (Points[0].X != 0)
        {
            Points.Insert(0, new Int2(0, 0));
        }

        if (Points[^1].X != 255)
        {
            Points.Add(new Int2(255, 255));
        }
    }

    public override SKBitmap GenerateLayer(SKBitmap groupBitmap)
    {
        // Build LUT - TODO
        // Conditions:
        // Contiguous, with first and second order derivative continuity, and curvature of zero at end points
        byte[] table = GenerateCurveLut(Points);

        // TODO
        const int clampMin = 0; // Control Point 0 y value
        const int clampMax = 255; // Control Point N-1 y value
        
        // Apply LUT
        SKColor[]? pixels = groupBitmap.Pixels;
        for (int i = 0; i < pixels.Length; i++)
        {
            int lum = (7471 * pixels[i].Blue + 38470 * pixels[i].Green + 19595 * pixels[i].Red) >> 16;
            int targetLum = table[lum];
            int delta = targetLum - lum;
            
            // 3. Apply the delta equally to R, G, and B and clamp to [0, 255]
            byte rFinal = (byte)Math.Clamp(pixels[i].Red + delta, clampMin, clampMax);
            byte gFinal = (byte)Math.Clamp(pixels[i].Green + delta, clampMin, clampMax);
            byte bFinal = (byte)Math.Clamp(pixels[i].Blue + delta, clampMin, clampMax);
            
            pixels[i] = new SKColor(rFinal, gFinal, bFinal, pixels[i].Alpha );
        }
        
        SKBitmap layer = new(groupBitmap.Info);
        layer.Pixels = pixels;

        SKBitmap output = groupBitmap.Paste(layer);

        return output;
    }

    public static byte[] GenerateCurveLut(IList<Int2> controlPoints)
    {
        if (controlPoints == null)
            throw new ArgumentNullException(nameof(controlPoints));

        // Sort points by X and deduplicate X coordinates (keeping the last point for identical X)
        var points = controlPoints
            .GroupBy(p => Math.Clamp(p.X, 0, 255))
            .Select(g => new Int2(g.Key, Math.Clamp(g.Last().Y, 0, 255)))
            .OrderBy(p => p.X)
            .ToArray();

        byte[] lut = new byte[256];

        if (points.Length == 0)
        {
            // Default identity curve
            for (int i = 0; i < 256; i++) lut[i] = (byte)i;
            return lut;
        }

        if (points.Length == 1)
        {
            // Flat horizontal line at the single point's Y value
            Array.Fill(lut, (byte)points[0].Y);
            return lut;
        }

        int n = points.Length;
        
        // Step 1: Compute second derivatives (M) via Tridiagonal Matrix Algorithm
        float[] m = GetSecondDerivatives(points);

        // Step 2: Evaluate spline for every intensity value 0..255
        int segment = 0;
        for (int xi = 0; xi < 256; xi++)
        {
            // Clamp flat ends outside the first and last control points
            if (xi <= points[0].X)
            {
                lut[xi] = (byte)Math.Clamp(points[0].Y, 0, 255);
                continue;
            }
            if (xi >= points[n - 1].X)
            {
                lut[xi] = (byte)Math.Clamp(points[n - 1].Y, 0, 255);
                continue;
            }

            // Advance to the active spline segment [x[segment], x[segment + 1]]
            while (segment < n - 2 && xi > points[segment + 1].X)
            {
                segment++;
            }

            double h = points[segment + 1].X - points[segment].X;
            double a = (points[segment + 1].X - xi) / h;
            double b = (xi - points[segment].X) / h;

            // Cubic spline polynomial evaluation
            double interpolatedY =
                a * points[segment].Y +
                b * points[segment + 1].Y +
                ((a * a * a - a) * m[segment] + (b * b * b - b) * m[segment + 1]) * (h * h) / 6.0;

            lut[xi] = (byte)Math.Clamp(Math.Round(interpolatedY), 0, 255);
        }

        return lut;
    }
    
    static float[] GetSecondDerivatives(Int2[] points)
    {
        var x = points.Select(p => (float)p.X).ToArray();
        var y = points.Select(p => (float)p.Y).ToArray();
        
        var n = points.Length;
        float[] output = new float[points.Length];

        output[0] = 0;
        output[points.Length - 1] = 0;

        if (points.Length == 2)
        {
            return output;
        }
        
        int interiorCount = n - 2;
        float[] lower = new float[interiorCount]; // Sub-diagonal (a)
        float[] diag = new float[interiorCount];  // Main diagonal (b)
        float[] upper = new float[interiorCount]; // Super-diagonal (c)
        float[] rhs = new float[interiorCount];   // Right-hand side (d)

        for (int i = 1; i < n - 1; i++)
        {
            int idx = i - 1;
            float hPrev = x[i] - x[i - 1];
            float hNext = x[i + 1] - x[i];

            lower[idx] = hPrev;
            diag[idx] = 2.0f * (hPrev + hNext);
            upper[idx] = hNext;
            rhs[idx] = 6.0f * (((y[i + 1] - y[i]) / hNext) - ((y[i] - y[i - 1]) / hPrev));
        }

        // Thomas Algorithm: Forward elimination
        for (int i = 1; i < interiorCount; i++)
        {
            float factor = lower[i] / diag[i - 1];
            diag[i] -= factor * upper[i - 1];
            rhs[i] -= factor * rhs[i - 1];
        }

        // Thomas Algorithm: Back substitution
        output[n - 2] = rhs[interiorCount - 1] / diag[interiorCount - 1];
        for (int i = interiorCount - 2; i >= 0; i--)
        {
            output[i + 1] = (rhs[i] - upper[i] * output[i + 2]) / diag[i];
        }

        return output;
    }
}
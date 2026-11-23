using System.Runtime.CompilerServices;
using SkiaSharp;

namespace TechnicolorPatcher.Util.Image;

// ReSharper disable once InconsistentNaming
public unsafe class SKBitmapPointer
{
    public IntPtr PixelPtr { get; init; }

    private byte* BaseBitmapPtr { get; }

    public int Width { get; init; }
    public int Height { get; init; }
    private int RowBytes { get; }

    public SKBitmapPointer(SKBitmap bitmap)
    {
        IntPtr bitmapPixelsPtr = bitmap.GetPixels();
        if (bitmapPixelsPtr == IntPtr.Zero)
        {
            throw new NullReferenceException();
        }
        
        Width = bitmap.Width;
        Height = bitmap.Height;
        RowBytes = bitmap.RowBytes;
        
        BaseBitmapPtr = (byte*)bitmapPixelsPtr.ToPointer();
    }

    public uint* GetRowBase(long y)
    {
        return (uint*)(BaseBitmapPtr + y * RowBytes);
    }
}

public class Common
{
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static float[] ToHsv(byte[] rgb)
    {
        float r = rgb[0] / 255.0f;
        float g = rgb[1] / 255.0f;
        float b = rgb[2] / 255.0f;
        
        float max = Math.Max(r, Math.Max(g, b));
        float min = Math.Min(r, Math.Min(g, b));
        float range = max - min;

        const float tolerance = 0.001f;
        
        float h;
        if (range == 0)
        {
            h = 0;
        }
        else if (Math.Abs(max - r) < tolerance)
        {
            h = (60f * ((g - b) / range) + 360f) % 360f;
        }
        else if (Math.Abs(max - g) < tolerance)
        {
            h = (60f * ((b - r) / range) + 120f) % 360f;
        }
        else if (Math.Abs(max - b) < tolerance)
        {
            h = (60f * ((r - g) / range) + 240f) % 360f;
        }
        else
        {
            h = 0;
        }

        float s;
        if (max == 0.0f)
        {
            s = 0;
        }
        else
        {
            s = (range / max) * 100.0f;
        }

        float v = max * 100.0f;

        return [h, s, v];
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static byte[] ToRgb(float[] hsv)
    {
        float h = hsv[0];
        float s = hsv[1] / 100f;
        float v = hsv[2] / 100f;
            
        float r, g, b;

        float c = v * s;
        
        float x = c * ( 1 - Math.Abs((h / 60f) % 2 - 1 ));

        float m = v - c;

        switch (h)
        {
            case < 60f:
                r = c;
                g = x;
                b = 0;
                break;
            case < 120f:
                r = x;
                g = c;
                b = 0;
                break;
            case < 180f:
                r = 0;
                g = c;
                b = x;
                break;
            case < 240f:
                r = 0;
                g = x;
                b = c;
                break;
            case < 300f:
                r = x;
                g = 0;
                b = c;
                break;
            default:
                r = c;
                g = 0;
                b = x;
                break;
        }

        return [(byte)((r + m) * 255), (byte)((g + m) * 255), (byte)((b + m) * 255)];
    }

    public static void Validate(params SKBitmap[] bitmaps)
    {
        foreach (SKBitmap bitmap in bitmaps)
        {
            if (bitmap.ColorType != SKColorType.Rgba8888)
            {
                throw new ArgumentException($"Invalid color type for image. Expected Rgba8888, got {bitmap.ColorType}");
            }
        
            if (bitmap.AlphaType != SKAlphaType.Unpremul)
            {
                throw new ArgumentException($"Invalid alpha type for image. Expected Unpremul, got {bitmap.AlphaType}");
            } 
        }

        if (bitmaps.Length > 1)
        {
            for (int index = 1; index < bitmaps.Length; index++)
            {
                SKBitmap bitmap = bitmaps[index];

                if (bitmap.Width != bitmaps[0].Width || bitmap.Height != bitmaps[0].Height)
                {
                    throw new ArgumentException("Width and height must match");
                }
            }
        }
    }
}
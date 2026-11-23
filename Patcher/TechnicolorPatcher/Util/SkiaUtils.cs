using System.Diagnostics;
using System.Runtime.InteropServices;
using BCnEncoder.Decoder;
using BCnEncoder.Shared;
using CommunityToolkit.HighPerformance;
using SkiaSharp;

namespace TechnicolorPatcher.Util;

public static class SkiaUtils
{
    // Assumes BG is fully opaque
    public static unsafe void Paste(this SKBitmap bitmap, SKBitmap overlay)
    {
        if (bitmap.AlphaType != SKAlphaType.Unpremul)
        {
            throw new ArgumentException($"Invalid alpha type for bitmap image: {bitmap.AlphaType}");
        }

        if (overlay.AlphaType != SKAlphaType.Unpremul)
        {
            throw new ArgumentException($"Invalid overlay type for alpha image: {overlay.AlphaType}");
        }
        
        if (bitmap.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for bitmap image. Expected Rgba8888, got {bitmap.ColorType}");
        }
        
        if (overlay.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for overlay image. Expected Rgba8888, got {overlay.ColorType}");
        }
        
        IntPtr bitmapPixelsPtr = bitmap.GetPixels();
        if (bitmapPixelsPtr == IntPtr.Zero)
        {
            throw new ArgumentException();
        }
        
        IntPtr overlayPixelsPtr = overlay.GetPixels();
        if (overlayPixelsPtr == IntPtr.Zero)
        {
            throw new ArgumentException();
        }

        int width = bitmap.Width;
        int height = bitmap.Height;
        int rowBytes = bitmap.RowBytes;
        
        byte* baseBitmapPtr = (byte*)bitmapPixelsPtr.ToPointer();
        byte* baseOverlayPtr = (byte*)overlayPixelsPtr.ToPointer();

        //Parallel.For(0L, height, y =>
        //{
        for (int y = 0; y < height; y++) 
        {
            // Calculate exact start of the row using RowBytes
            uint* rowBase = (uint*)(baseBitmapPtr + y * rowBytes);
            uint* rowOverlay = (uint*)(baseOverlayPtr + y * rowBytes);
        
            for (int x = 0; x < width; x++)
            {
                byte rBg = (byte)((rowBase[x] >> 0) & 0xFF);
                byte gBg = (byte)((rowBase[x] >> 8) & 0xFF);
                byte bBg = (byte)((rowBase[x] >> 16) & 0xFF);
                
                byte rFg = (byte)((rowOverlay[x] >> 0) & 0xFF);
                byte gFg = (byte)((rowOverlay[x] >> 8) & 0xFF);
                byte bFg = (byte)((rowOverlay[x] >> 16) & 0xFF);
                byte aFg = (byte)((rowOverlay[x] >> 24) & 0xFF);

                const byte aOut = 255;
                byte rOut = (byte)Math.Clamp((aFg * rFg + (255 - aFg) * rBg) / 255, 0, 255);
                byte gOut = (byte)Math.Clamp((aFg * gFg + (255 - aFg) * gBg) / 255, 0, 255);
                byte bOut = (byte)Math.Clamp((aFg * bFg + (255 - aFg) * bBg) / 255, 0, 255);

                rowBase[x] = (uint)(aOut << 24 | bOut << 16 | gOut << 8 | rOut);
            }
        }
    }

    public static SKBitmap AlphaToGrayscale(SKBitmap bitmap)
    {
        if (bitmap.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for image. Expected Rgba8888, got {bitmap.ColorType}");
        }
        
        SKBitmap result = new(bitmap.Width, bitmap.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        
        ReadOnlySpan<byte> cSpan = bitmap.GetPixelSpan();

        Span<byte> resultSpan = result.GetPixelSpan();
        
        for (int i = 0; i < cSpan.Length; i += 4)
        {
            resultSpan[i + 0] = cSpan[i + 3];
            resultSpan[i + 1] = cSpan[i + 3];
            resultSpan[i + 2] = cSpan[i + 3];
            resultSpan[i + 3] = 255;
        }

        return result;
    }

    public static float[] ToHSV(byte[] rgb)
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

    public static byte[] ToRGB(float[] hsv)
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

    public static unsafe void AdjustBrightness(this SKBitmap bitmap, float percent)
    {
        ArgumentOutOfRangeException.ThrowIfGreaterThan(percent, 2.0f);

        if (bitmap.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type: {bitmap.ColorType}");
        }
        
        IntPtr pixelsPtr = bitmap.GetPixels();
        if (pixelsPtr == IntPtr.Zero)
        {
            return;
        }

        byte[] lut = new byte[256];
        for (int i = 0; i < 256; i++)
        {
            lut[i] = (byte)Math.Clamp(Math.Round(i * percent), 0, 255);
        }

        int width = bitmap.Width;
        int height = bitmap.Height;
        int rowBytes = bitmap.RowBytes;
        byte* basePtr = (byte*)pixelsPtr.ToPointer();

        Parallel.For(0, height, y =>
        {
            // Calculate exact start of the row using RowBytes
            uint* row = (uint*)(basePtr + y * rowBytes);
        
            for (int x = 0; x < width; x++)
            {
                uint pixel = row[x];
                byte r = (byte)((pixel >> 0) & 0xFF);
                byte g = (byte)((pixel >> 8) & 0xFF);
                byte b = (byte)((pixel >> 16) & 0xFF);
                byte a = (byte)((pixel >> 24) & 0xFF);
                
                row[x] = (uint)((a << 24) | (lut[b] << 16) | (lut[g] << 8) | lut[r]);
            }
        });
    }

    public static unsafe void AdjustSaturation(this SKBitmap bitmap, float percent)
    {
        if (bitmap.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type: {bitmap.ColorType}");
        }
        
        IntPtr pixelsPtr = bitmap.GetPixels();
        if (pixelsPtr == IntPtr.Zero)
        {
            return;
        }

        uint[,,] lut = new uint[256,256,256];
        for (int r = 0; r < 256; r++)
        {
            for (int g = 0; g < 256; g++)
            {
                for (int b = 0; b < 256; b++)
                {
                    byte[] rgb = [(byte)r,(byte)g,(byte)b];
                    float[] hsv = ToHSV(rgb);
                    hsv[1] = Math.Clamp(hsv[1] * percent, 0, 100.0f);
                    byte[] rgb2 = ToRGB(hsv);
                    lut[r, g, b] = (uint)(255 << 24 | rgb2[0] << 16 | rgb2[1] << 8 | rgb2[2]);
                }
            }
        }

        int width = bitmap.Width;
        int height = bitmap.Height;
        int rowBytes = bitmap.RowBytes;
        byte* basePtr = (byte*)pixelsPtr.ToPointer();

        Parallel.For(0L, height, y =>
        {
            // Calculate exact start of the row using RowBytes
            uint* row = (uint*)(basePtr + y * rowBytes);
        
            for (int x = 0; x < width; x++)
            {
                uint pixel = row[x];
                byte b = (byte)(pixel & 0xFF);
                byte g = (byte)((pixel >> 8) & 0xFF);
                byte r = (byte)((pixel >> 16) & 0xFF);
                byte a = (byte)((pixel >> 24) & 0xFF);
                // Direct pointer read/write with zero bounds checks
                
                uint rgbNew = lut[r, g, b];

                row[x] = ((uint)a << 24) | rgbNew;
            }
        });
    }

    public static unsafe SKBitmap MergeBitmaps(SKBitmap color, SKBitmap alpha)
    {
        if (color.AlphaType != SKAlphaType.Unpremul)
        {
            throw new ArgumentException($"Invalid alpha type for color image: {color.AlphaType}");
        }

        if (alpha.AlphaType != SKAlphaType.Unpremul)
        {
            throw new ArgumentException($"Invalid alpha type for alpha image: {color.AlphaType}");
        }
        
        if (color.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for color image. Expected Rgba8888, got {color.ColorType}");
        }
        
        if (alpha.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for alpha image. Expected Rgba8888, got {alpha.ColorType}");
        }
        
        SKBitmap result = new(color.Width, color.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        
        IntPtr colorPixelsPtr = color.GetPixels();
        if (colorPixelsPtr == IntPtr.Zero)
        {
            throw new ArgumentException();
        }
        
        IntPtr alphaPixelsPtr = alpha.GetPixels();
        if (alphaPixelsPtr == IntPtr.Zero)
        {
            throw new ArgumentException();
        }
        
        IntPtr resultPixelsPtr = result.GetPixels();
        if (resultPixelsPtr == IntPtr.Zero)
        {
            throw new ArgumentException();
        }

        int width = result.Width;
        int height = result.Height;
        int rowBytes = result.RowBytes;
        
        byte* baseColorPtr = (byte*)colorPixelsPtr.ToPointer();
        byte* baseAlphaPtr = (byte*)alphaPixelsPtr.ToPointer();
        byte* baseResultPtr = (byte*)resultPixelsPtr.ToPointer();

        //Parallel.For(0L, height, y =>
        //{
        for (int i = 0; i < height; i++) 
        {
            // Calculate exact start of the row using RowBytes
            uint* rowColor = (uint*)(baseColorPtr + i * rowBytes);
            uint* rowAlpha = (uint*)(baseAlphaPtr + i * rowBytes);
            uint* rowResult = (uint*)(baseResultPtr + i * rowBytes);
        
            for (int x = 0; x < width; x++)
            {
                byte r = (byte)((rowColor[x] >> 0) & 0xFF);
                byte g = (byte)((rowColor[x] >> 8) & 0xFF);
                byte b = (byte)((rowColor[x] >> 16) & 0xFF);
                byte a = (byte)((rowAlpha[x] >> 0) & 0xFF);
                
                rowResult[x] = (uint)(a << 24 | b << 16 | g << 8 | r);
            }
        };

        return result;
    }

    public static void ClearAlpha(this SKBitmap bitmap)
    {
        if (bitmap.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for image. Expected Rgba8888, got {bitmap.ColorType}");
        }
        
        if (bitmap.AlphaType != SKAlphaType.Unpremul)
        {
            throw new ArgumentException($"Invalid alpha type for image. Expected Unpremul, got {bitmap.AlphaType}");
        }
        
        Span<byte> bitmapSpan = bitmap.GetPixelSpan();
        
        for (int i = 0; i < bitmapSpan.Length; i += 4)
        {
            bitmapSpan[i + 3] = 255;
        }
    }

    public static void ReplaceWithAlpha(this SKBitmap bitmap)
    {
        if (bitmap.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for image. Expected Rgba8888, got {bitmap.ColorType}");
        }
        
        if (bitmap.AlphaType != SKAlphaType.Unpremul)
        {
            throw new ArgumentException($"Invalid alpha type for image. Expected Unpremul, got {bitmap.AlphaType}");
        }
        
        Span<byte> bitmapSpan = bitmap.GetPixelSpan();
        
        for (int i = 0; i < bitmapSpan.Length; i += 4)
        {
            bitmapSpan[i + 0] = bitmapSpan[i + 3];
            bitmapSpan[i + 1] = bitmapSpan[i + 3];
            bitmapSpan[i + 2] = bitmapSpan[i + 3];
            //bitmapSpan[i + 3] = bitmapSpan[i + 3];
        }
    }

    public static SKBitmap MergeBitmaps(SKBitmap red, SKBitmap green, SKBitmap blue, SKBitmap alpha)
    {
        if (red.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for red image. Expected Rgba8888, got {red.ColorType}");
        }
        
        if (green.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for green image. Expected Rgba8888, got {green.ColorType}");
        }
        
        if (blue.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for blue image. Expected Rgba8888, got {blue.ColorType}");
        }
        
        if (alpha.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for alpha image. Expected Rgba8888, got {alpha.ColorType}");
        }
        
        SKBitmap result = new(red.Width, red.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        
        ReadOnlySpan<byte> rSpan = red.GetPixelSpan();
        ReadOnlySpan<byte> gSpan = green.GetPixelSpan();
        ReadOnlySpan<byte> bSpan = blue.GetPixelSpan();
        ReadOnlySpan<byte> aSpan = alpha.GetPixelSpan();
            
        Span<byte> resultSpan = result.GetPixelSpan();
        
        for (int i = 0; i < rSpan.Length; i += 4)
        {
            resultSpan[i] = rSpan[i];
        }
        for (int i = 1; i < rSpan.Length; i += 4)
        {
            resultSpan[i] = gSpan[i];
        }
        for (int i = 2; i < rSpan.Length; i += 4)
        {
            resultSpan[i] = bSpan[i];
        }
        for (int i = 3; i < rSpan.Length; i += 4)
        {
            resultSpan[i] = aSpan[i - 3]; // Use red channel
        }

        return result;
    }
    
    public static SKBitmap LoadDds(string filePath)
    {
        using FileStream fs = File.OpenRead(filePath);
        BcDecoder decoder = new BcDecoder();

        // 1. Decode the DDS file into a 2D array of RGBA32 pixels
        Memory2D<ColorRgba32> decodedPixels = decoder.Decode2D(fs);

        int width = decodedPixels.Width;
        int height = decodedPixels.Height;

        // 2. Create an SKBitmap matching the RGBA8888 byte layout of ColorRgba32
        SKImageInfo imageInfo = new SKImageInfo(width, height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        SKBitmap bitmap = new SKBitmap(imageInfo);

        // 3. Copy the decoded pixel data into the SKBitmap's unmanaged memory buffer
        Span<byte> destinationBytes = bitmap.GetPixelSpan();
        int rowByteSize = width * 4; // 4 bytes per pixel (R, G, B, A)

        for (int y = 0; y < height; y++)
        {
            ReadOnlySpan<ColorRgba32> sourceRow = decodedPixels.Span.GetRowSpan(y);
            ReadOnlySpan<byte> sourceRowBytes = MemoryMarshal.AsBytes(sourceRow);

            Span<byte> destinationRowBytes = destinationBytes.Slice(y * bitmap.RowBytes, rowByteSize);
            sourceRowBytes.CopyTo(destinationRowBytes);
        }

        return bitmap;
    }

    public static void SaveDds(this SKBitmap bitmap, FileInfo filePath)
    {
        // Save PNG File
        SKData? image = SKImage.FromBitmap(bitmap).Encode(SKEncodedImageFormat.Png, 100);
        FileStream stream = new(filePath.FullName, FileMode.Create, FileAccess.Write);
        image.SaveTo(stream);
        stream.Close();

        if (Patcher.TexConvPath != null)
        {
            // Convert to DDS
            ProcessStartInfo startInfo = new()
            {
                CreateNoWindow = true,
                UseShellExecute = false,
                FileName = Patcher.TexConvPath.FullName,
                WindowStyle = ProcessWindowStyle.Hidden,
                Arguments = $"-y -f BC7_UNORM -o \"{filePath.Directory!.FullName}\" \"{filePath.FullName}\"",
                RedirectStandardOutput = true
            };

            using Process? process = Process.Start(startInfo);
            if (process != null)
            {
                process.WaitForExit();
                if (process.ExitCode != 0)
                {
                    var texconvOutput = ""; 
                    while (!process.StandardOutput.EndOfStream)
                    {
                        texconvOutput += process.StandardOutput.ReadLine();
                        texconvOutput += "\n";
                    }
                    throw new InvalidOperationException($"Texconv process failed with exit code {process.ExitCode}:\n{texconvOutput}");
                }
            }
            
            // Delete PNG
            filePath.Delete();
        }
    }

    public static void SavePng(this SKBitmap bitmap, string filePath)
    {
        bitmap.SavePng(new FileInfo(@"C:\Users\coldrifting\desktop\" + filePath));
    }
    
    public static void SavePng(this SKBitmap bitmap, FileInfo filePath)
    {
        byte[]? bytes = bitmap.Encode(SKEncodedImageFormat.Png, 100).ToArray();
        File.WriteAllBytes(filePath.FullName, bytes);
    }
}
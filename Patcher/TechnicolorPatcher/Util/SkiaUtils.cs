using System.Diagnostics;
using System.Runtime.InteropServices;
using BCnEncoder.Decoder;
using BCnEncoder.Shared;
using CommunityToolkit.HighPerformance;
using SkiaSharp;

namespace TechnicolorPatcher.Util;

public static class SkiaUtils
{
    public static SKBitmap Paste(this SKBitmap baseBitmap, SKBitmap overlayBitmap)
    {
        SKBitmap result = new SKBitmap(baseBitmap.Width, baseBitmap.Height,  SKColorType.Rgba8888, SKAlphaType.Premul);
        
        using SKCanvas canvas = new(result);
        canvas.Clear(SKColors.Transparent);
        canvas.DrawBitmap(baseBitmap, 0, 0, SKSamplingOptions.Default);
        canvas.DrawBitmap(overlayBitmap, 0, 0, SKSamplingOptions.Default);
        canvas.Flush();

        return result;
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

    public static SKBitmap MergeBitmaps(SKBitmap color, SKBitmap alpha)
    {
        if (color.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for color image. Expected Rgba8888, got {color.ColorType}");
        }
        
        if (alpha.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for alpha image. Expected Rgba8888, got {alpha.ColorType}");
        }
        
        SKBitmap result = new(color.Width, color.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        
        ReadOnlySpan<byte> cSpan = color.GetPixelSpan();
        ReadOnlySpan<byte> aSpan = alpha.GetPixelSpan();
            
        Span<byte> resultSpan = result.GetPixelSpan();
        
        for (int i = 0; i < cSpan.Length; i += 4)
        {
            resultSpan[i] = cSpan[i];
            resultSpan[i + 1] = cSpan[i + 1];
            resultSpan[i + 2] = cSpan[i + 2];
            resultSpan[i + 3] = aSpan[i];
        }

        return result;
    }

    public static SKBitmap ReplaceWithAlpha(SKBitmap bitmap)
    {
        if (bitmap.ColorType != SKColorType.Rgba8888)
        {
            throw new ArgumentException($"Invalid color type for red image. Expected Rgba8888, got {bitmap.ColorType}");
        }
        
        SKBitmap result = new(bitmap.Width, bitmap.Height, SKColorType.Rgba8888, SKAlphaType.Unpremul);
        
        ReadOnlySpan<byte> bitmapSpan = bitmap.GetPixelSpan();
            
        Span<byte> resultSpan = result.GetPixelSpan();
        
        for (int i = 0; i < bitmapSpan.Length; i += 4)
        {
            resultSpan[i + 0] = bitmapSpan[i + 3];
            resultSpan[i + 1] = bitmapSpan[i + 3];
            resultSpan[i + 2] = bitmapSpan[i + 3];
            resultSpan[i + 3] = bitmapSpan[i + 3];
        }

        return result;
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
            resultSpan[i] = aSpan[i];
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
        bitmap.SavePng(new FileInfo(filePath));
    }
    
    public static void SavePng(this SKBitmap bitmap, FileInfo filePath)
    {
        byte[]? bytes = bitmap.Encode(SKEncodedImageFormat.Png, 100).ToArray();
        File.WriteAllBytes(filePath.FullName, bytes);
    }
}
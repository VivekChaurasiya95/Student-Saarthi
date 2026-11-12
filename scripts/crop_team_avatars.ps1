Add-Type -AssemblyName System.Drawing

$outDir = "d:\Student Saarthi\static\images\team"
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}

$crops = @(
    @{
        Name = "vivek.jpg"
        Src = "C:/Users/Vivek Chaurasiya/.gemini/antigravity/brain/a5c74d64-3f55-4531-bfee-ffbe3300e046/.user_uploaded/media_1794507446502_a17a8241.jpg"
        X = 140
        Y = 65
        Size = 470
    },
    @{
        Name = "prajwal.jpg"
        Src = "C:/Users/Vivek Chaurasiya/.gemini/antigravity/brain/a5c74d64-3f55-4531-bfee-ffbe3300e046/.user_uploaded/media_1794507588912_4249434d.jpg"
        X = 200
        Y = 70
        Size = 420
    },
    @{
        Name = "atul.jpg"
        Src = "C:/Users/Vivek Chaurasiya/.gemini/antigravity/brain/a5c74d64-3f55-4531-bfee-ffbe3300e046/.user_uploaded/media_1794507600692_7052cb9d.jpg"
        X = 160
        Y = 125
        Size = 430
    }
)

foreach ($c in $crops) {
    $srcImg = [System.Drawing.Image]::FromFile($c.Src)
    
    # Destination 500x500 square bitmap
    $targetSize = 500
    $destBmp = New-Object System.Drawing.Bitmap($targetSize, $targetSize)
    $g = [System.Drawing.Graphics]::FromImage($destBmp)
    
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    
    $srcRect = New-Object System.Drawing.Rectangle($c.X, $c.Y, $c.Size, $c.Size)
    $destRect = New-Object System.Drawing.Rectangle(0, 0, $targetSize, $targetSize)
    
    $g.DrawImage($srcImg, $destRect, $srcRect, [System.Drawing.GraphicsUnit]::Pixel)
    
    # Save with 95% JPEG quality
    $codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
    $encoderParams = New-Object System.Drawing.Imaging.EncoderParameters(1)
    $encoderParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]95)
    
    $outPath = Join-Path $outDir $c.Name
    $destBmp.Save($outPath, $codec, $encoderParams)
    
    $g.Dispose()
    $destBmp.Dispose()
    $srcImg.Dispose()
    
    Write-Output "Generated: $outPath (500x500)"
}

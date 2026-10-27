# Fallback local server for Windows machines without Python.
# Serves the course (site/) at http://localhost:<port>/ (this computer only) and opens the hub.
param([int]$Port = 8000, [switch]$NoBrowser)

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\site")).Path
$Mime = @{
  ".html"="text/html; charset=utf-8"; ".htm"="text/html; charset=utf-8"; ".css"="text/css";
  ".js"="text/javascript"; ".mjs"="text/javascript"; ".json"="application/json";
  ".ipynb"="application/json"; ".wasm"="application/wasm"; ".zip"="application/zip";
  ".png"="image/png"; ".jpg"="image/jpeg"; ".jpeg"="image/jpeg"; ".gif"="image/gif";
  ".webp"="image/webp"; ".svg"="image/svg+xml"; ".ico"="image/x-icon"; ".pdf"="application/pdf";
  ".md"="text/markdown; charset=utf-8"; ".txt"="text/plain; charset=utf-8"; ".xml"="application/xml";
  ".yaml"="text/plain; charset=utf-8"; ".woff"="font/woff"; ".woff2"="font/woff2"; ".ttf"="font/ttf";
  ".docx"="application/vnd.openxmlformats-officedocument.wordprocessingml.document";
  ".pptx"="application/vnd.openxmlformats-officedocument.presentationml.presentation"
}

$listener = $null
for ($p = $Port; $p -lt $Port + 50; $p++) {
  try {
    $listener = New-Object System.Net.HttpListener
    $listener.Prefixes.Add("http://localhost:$p/")
    $listener.Start()
    $Port = $p
    break
  } catch { $listener = $null }
}
if ($null -eq $listener) { Write-Host "Could not open a local port."; exit 1 }

$url = "http://localhost:$Port/index.html"
Write-Host "Aayat-AP-Prep is running offline at $url"
Write-Host "Keep this window open while you work. Close it to stop."
if (-not $NoBrowser) { Start-Process $url }

while ($listener.IsListening) {
  $ctx = $listener.GetContext()
  $res = $ctx.Response
  try {
    $rel = [Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath).TrimStart("/")
    if ($rel -eq "" -or $rel.EndsWith("/")) { $rel = $rel + "index.html" }
    $full = [IO.Path]::GetFullPath((Join-Path $Root $rel))
    if (-not ($full + "\").StartsWith($Root.TrimEnd("\") + "\", [StringComparison]::OrdinalIgnoreCase)) {
      $res.StatusCode = 403
    } elseif (Test-Path $full -PathType Container) {
      $res.StatusCode = 301
      $res.RedirectLocation = $ctx.Request.Url.AbsolutePath.TrimEnd("/") + "/"
    } elseif (Test-Path $full -PathType Leaf) {
      $ext = [IO.Path]::GetExtension($full).ToLower()
      $res.ContentType = $(if ($Mime.ContainsKey($ext)) { $Mime[$ext] } else { "application/octet-stream" })
      $bytes = [IO.File]::ReadAllBytes($full)
      $res.ContentLength64 = $bytes.Length
      $res.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
      $res.StatusCode = 404
    }
  } catch {
    $res.StatusCode = 500
  } finally {
    $res.OutputStream.Close()
  }
}

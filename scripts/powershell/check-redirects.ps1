# Check status codes for a list of source URLs and expected targets.
# CSV columns: source_url,target_url
Param([string]$CsvPath = "tech-seo/redirect-map-template.csv")

$rows = Import-Csv $CsvPath
foreach ($r in $rows) {
  try {
    $resp = Invoke-WebRequest -Uri $r.source_url -MaximumRedirection 0 -ErrorAction Stop
    Write-Host "$($r.source_url) -> $($resp.StatusCode)"
  } catch {
    if ($_.Exception.Response) {
      $code = $_.Exception.Response.StatusCode.value__
      $loc = $_.Exception.Response.Headers['Location']
      Write-Host "$($r.source_url) -> $code (Location: $loc)"
    } else {
      Write-Host "$($r.source_url) -> ERROR: $($_.Exception.Message)"
    }
  }
}

param(
  [Parameter(Mandatory=$true)][string]$UpstreamPath
)
$ErrorActionPreference = "Stop"
$expected = "9d5d05de7f4ccf39840224ed295f292ab8aeb598"
$actual = (git -C $UpstreamPath rev-parse HEAD).Trim()
if ($actual -ne $expected) { throw "Upstream commit mismatch: expected $expected, got $actual" }
wsl.exe bash -lc "cd '$($UpstreamPath.Replace('C:\','/mnt/c/').Replace('\','/'))/c' && make olmoe"
if ($LASTEXITCODE -ne 0) { throw "Colibri OLMoE build failed" }
Write-Output "Verified Colibri $actual (target: c/olmoe)"


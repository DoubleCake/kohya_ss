#批量存放运行脚本的路径，可以根据自己存放训练脚本的路径进行调整
$folderPath = ".\BatchTrainFolders" 

$scripts = Get-ChildItem -Path $folderPath -Filter "*.ps1" -File

foreach($script in $scripts){
    Write-Host "Start Train: $($script.Name)"
    &$script.FullName
}

Pause
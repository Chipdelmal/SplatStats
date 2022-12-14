# Docker Bundle

## Installation and Setup


```bash
data
    jsons
        config.txt
        export-*
    battles
        *.pkl
    out
        *.png
        *.csv
```

## How to Run

```bash
docker run \
    --net=host \
    -v "$(pwd)":/data/ \
    splatstats:dev \
    --player "čħîþ ウナギ" --weapon "Hero Shot Replica" --battleMode "All" \
    --download "True" --upload "True"
```

Docker call breakdown:

* `--net=host`: Needed if `--upload` or `--download` are `True`, as [s3s](https://github.com/frozenpandaman/s3s)  needs internet connection for scraping.
* `-v "$(pwd)":/data/`
* `splatstats:dev`: Docker image name and version

SplatStat's optional arguments:

* `--player`: Username string (Defaults to `"None"` and skips SplatStats)
* `--weapon`: Weapon's string (Defaults to `"All"`)
* `--matchMode`: Match mode string (Defaults to `"All"`)
* `--download`: Determines if [s3s](https://github.com/frozenpandaman/s3s) should be used to download the data (Defaults to `"False"`)
* `--upload`: Determines if [s3s](https://github.com/frozenpandaman/s3s) should be used to upload the missing data to stat.ink (Defaults to "False")

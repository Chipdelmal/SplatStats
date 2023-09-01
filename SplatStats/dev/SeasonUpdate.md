# Instructions for Season Updates


1. Add the new stages to the stages color dictionary in the `constants.py` file.
2. Download the [weapons](https://stat.ink/api-info/weapon3) and [stages](https://stat.ink/api-info/stage3) JSONs
3. Update the weapons dictionary on the `statInkConstants.py` file with the JSON reader (remember to comment line out).
4. Update s3s version on the `other` folder (copy new `s3s.py` file and paste the commented lines).
5. Update the stages dictionary on `statInkConstants.py` manually.
6. Update both docker images (splats and inkstat).
7. Push to docker.
8. Push to pypi.
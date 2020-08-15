# Installation
Copy the `mayan_custom_app` folder to somewhere in your PYTHONPATH. When using Mayan with docker-compose, the easiest way would be to clone this git repo to `/my/repo/path/mayan-custom-app` and add the line

```
  mayan:

    ...other sections...

    volumes:

      ... other volumes...

      - /my/repo/path/mayan-custom-app/mayan_custom_app:/var/lib/mayan/mayan_custom_app
```

to your `docker-compose.yml`.

Afterwards, go to `System -> Setup -> Settings -> Common` in the Mayan web interface and edit the `COMMON_EXTRA_APPS` setting to the value
```
- mayan_custom_app
```

Finally, restart Mayan.
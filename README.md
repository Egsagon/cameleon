# CAMeleon

Quick camera switcher based on camera motion.

### Installation

```sh
git clone https://github.com/Egsagon/cameleon
cd cameleon
chmod +x cameleon
sudo cp cameleon /usr/bin/
```

### Usage
```sh
cameleon
```

### Settings

Edit `settings.json` as this format:
```jsonc
{
    "pause": true,      // Wether to pause the curent track
    "group": 2,         // Switch to nth workspace (null for none)
    "command": null     // Additional commands
}
```


### TODO
Change rel settings path to raw path

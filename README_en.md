# getas — Retrieve AS information and routes
<img src="getas_banner.jpg" alt="getas by Mikhail Barinov - Retrieve AS information and routes" width=100% align=center >

- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Using getas on Windows](#using-getas-on-windows)
- [Screenshots](#screenshots)

`getas` is a convenient tool for analyzing `Autonomous Systems` (AS) information, routes, and `network aggregation`. The script supports working with IP addresses, networks, domain names, or AS numbers. Its key features include retrieving detailed `AS` information, aggregating networks, and formatted output in both `English` and `Russian`.

This tool is designed for network engineers, analysts, and anyone interested in Internet route analysis.

*With many websites being blocked, up-to-date information about networks associated with various organizations has become particularly valuable. For example, to get a full list of networks associated with YouTube (Google), you only need to run:*
```
getas youtube.com -r
```


### Install dependencies

The script requires Python 3 and the whois command. Install them if they are not already available:

#### Debian/Ubuntu:
```
sudo apt update
sudo apt install python3 python3-pip whois
```

#### RHEL/CentOS:
```
sudo dnf install python3 python3-pip whois
```


### Install the script

To make the script easier to use, create a symbolic link:

```
sudo ln -s $(pwd)/getas.py /usr/local/bin/getas
```

Now you can run the script using the command `getas`.

### Recommended language configuration

By default, the script outputs information in English. To set Russian as the default language, add the following alias to your `.bashrc` file:

```
echo "alias getas='getas --lang ru'" >> ~/.bashrc source ~/.bashrc
```


---

## Usage Examples

### Retrieve AS information by AS number and advertised networks:

```
getas 15169
```

### Set a tolerance level for network aggregation:

```
getas 15169 --tolerance 8
```

### Prevent network aggregation:

```
getas 15169 --no-merge
```

### Retrieve AS information by IP address:

```
getas 8.8.8.8
```

### Retrieve AS information for an IP and its advertised networks:

```
getas 8.8.8.8 -r
```

### Convert subnet masks to binary format:

```
getas 8.8.8.8 -m -r
```

### Retrieve AS information using a domain name:

```
getas example.com
```

### Change output language:
```
getas mbarinov.ru -r --lang {ru,en}
```

### Help:

```
getas --help
getas help
```


---

## Using getas on Windows

To run the `getas.py` script on Windows, you need to set up Python and follow a few steps:

### Step 1. Install Python

- Download Python from the [official website](https://www.python.org/downloads/).
- Install `Python`, ensuring that the `Add Python to PATH` option is selected during installation.
- Verify the installation by running the following command in the Command Prompt:

# Update Reel Control System Software

I tested this using my Linux/Ubuntu machine.

## Preparation

You will need to have a computer connected to the cable reel via network. You will also need to updated Docker images. You will also need the updated Docker images (`rcs-api-prod.tar` and `rcs-web-prod.tar`).

## Raspberry Pi Login Credentials

**User**: `reach-admin`
**Password**: `reachadmin`
For the host IP address I will be using `192.168.1.107` as an example. You will need to use the IP address of your particular cable reel.

## Copy files to raspberry pi

- Copy files to USB drive, mount to cable reel and copy from there
- Use SSH/SCP (recommended)

### SCP

```bash
scp rcs-api-prod.tar rcs-web-prod.tar reach-admin@192.168.1.107:~/
```

#### Stop Reel Control Service

SSH into the host and stop the service.

```bash
ssh reach-admin@192.168.1.107
sudo systemctl stop reel-control-system.service
```

#### Backup Existing Docker Images

We will backup the existing Docker images by creating new tags.

```bash
docker tag rcs-api-prod:latest rcs-api-prod:backup1
docker tag rcs-web-prod:latest rcs-web-prod:backup1
```

Then remove the original latest tags:

```bash
docker rmi rcs-api-prod:latest rcs-web-prod:latest
```

#### Load New Docker Images

Load the archived images into the Docker engine

```bash
docker load -i rcs-api-prod.tar
docker load -i rcs-web-prod.tar
```

Confirm they have been loaded using

```bash
docker images
```

#### Start Reel Control Service

```bash
sudo systemctl start reel-control-system.service 
```

You can verify the docker containers are now running

```bash
docker ps
```

#### Troubleshooting

If you encounter any issues, you can restore the backup images:

```bash
docker tag rcs-api-prod:backup1 rcs-api-prod:latest
docker tag rcs-web-prod:backup1 rcs-web-prod:latest
sudo systemctl restart reel-control-system.service
```

# XML to JSON App Setup Guide

This guide will walk you through the steps to set up the XML to JSON app on Google Cloud Run using the Google Cloud Console and automatically update the container when you push changes to a GitHub repository.

## Prerequisites

Before you begin, make sure you have the following:

- A Google Cloud account
- A project created in the Google Cloud Console
- A GitHub account and a repository containing your XML to JSON app code

## Step 1: Enable the required APIs

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Select your project from the project dropdown menu.
3. In the navigation menu, go to "APIs & Services" > "Library".
4. Search for and enable the following APIs:
   - Cloud Run API
   - Cloud Build API

## Step 2: Connect your GitHub repository

1. In the Google Cloud Console, go to the Cloud Run page.
2. Click on "Create Service".
3. Select "Continuously deploy new revisions from a source repository".
4. Click "Set up with Cloud Build".
5. In the "Connect to a repository" section, click "GitHub".
6. Authorize Google Cloud Run to access your GitHub account.
7. Select the repository containing your XML to JSON app code.
8. Choose the branch you want to use for deployment (e.g., "main" or "master").
9. Click "Next".

## Step 3: Configure the container settings

1. In the "Build Configuration" section, select "Dockerfile" as the build type.
2. Specify the path to your Dockerfile within the repository.
3. Set the port to `8080`.
4. Under "Environment variables", add the following variables:
   - `AUTH_USERNAME`: The username for authentication.
   - `AUTH_PASSWORD`: The password for authentication.
   - `XANO_URL`: The URL of your Xano endpoint.
   - `XANO_KEY`: the x-api-key authorization header of your Xano endpoint. Refer to this guide: https://www.youtube.com/watch?v=n8RRMycLOdE&pp=ygUiY3JlYXRlIGFwaSBrZXkgaW4geGFubyBzdGF0ZWNoYW5nZQ%3D%3D
   - `XML_FILE_URL`: The URL of the XML file to be processed.
5. Click "Next".

## Step 4: Configure the service settings

1. Enter a name for your service, e.g., "xml-to-json-app".
2. Choose a region for your service.
3. Under "Authentication", select "Allow unauthenticated invocations" to make the service publicly accessible.
4. Under "Memory allocated", select an appropriate amount of memory for your service.
5. Under "Maximum number of instances", set the desired maximum number of instances for auto-scaling.
6. Under "Ingress", select "Allow all traffic".
7. Click "Create".

## Step 5: Trigger the XML to JSON conversion

1. Once the service is deployed, you will see its URL in the Cloud Run page.
2. To trigger the XML to JSON conversion, send a POST request to the service URL with the `/trigger` endpoint.
   - Example:
   - curl -X POST -u username:password https://your-service-url.run.app/trigger
3. The service will download the XML file, decompress it (if necessary), parse it into JSON, and send the jobs to your Xano endpoint.

## Step 6: Automatic container updates

1. Whenever you push changes to your connected GitHub repository branch, Google Cloud Build will automatically build a new container image based on your updated code.
2. Once the build is successful, the new container image will be deployed to your Cloud Run service, replacing the previous version.
3. You can view the build logs and deployment status in the Cloud Run page or the Cloud Build page.

That's it! Your XML to JSON app is now set up on Google Cloud Run, and it will automatically update whenever you push changes to your connected GitHub repository.

Note: Make sure to replace the placeholders (e.g., `AUTH_USERNAME`, `AUTH_PASSWORD`, `XANO_URL`, `XML_FILE_URL`) with your actual values in the environment variables section during the setup process.

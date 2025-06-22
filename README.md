# DAG Designer - The AI Agent to help with all your design needs

This is my submission for the Folio Canva Challenge: AI Agents - June 2025.

I was extremely challenged with this project and learned a lot of new tools. This is my first time building a full stack application and have never used typescript prior to this challenge.

### Project Outline

- Problem: Beginner designers often struggle with basic design principles and may not always have the resources to ask for help. Additionally, the friction to edit images can cause delays in workflow and may be limited by photoshop skills or other editing tools.
- Objective: DAG addresses the need for design advice and the ability to edit images on the fly solely using natural language.
- Capabilities: DAG has the capability to autonomously retrieve your design and edit and replace images directly within Canva. To edit an image, simply select the image on the design and ask DAG to bring your idea to life.

### Project Design and Setup

The backend of this project was written in Python using FastAPI. The agent system used OpenAI's new agents library, openai-agents, and the gpt-image-1 model for requests.
The frontend utilized Canva's Gen AI app template.

Buzzword collection of tools used: SQLite Database, AWS S3, React, TypeScript, Python, OpenAI, OpenAI-Agents, FastAPI

Canva tools: This project uses both the Apps SDK and the Connect API so the setup is slightly involved.

#### Future Works

Since this was my first time developing a fullstack application, there are security concerns to address for the backend and frontend. I believe the backend is modular enough to allow for improving on this in the future.
Secondary features: Allowing the agent to generate any image rather than exclusively selecting and editing an image. Improved UI/UX.

Note: Since the OpenAI API Key uses the gpt-image-1 model, they require personal identification verification. If this is an issue, please contact me and I will provide an API Key from my project. Similarly for the S3 Bucket.

## Requirements

- Node.js `v18` or `v20.10.0`
- npm `v9` or `v10`

**Note:** To make sure you're running the correct version of Node.js, we recommend using a version manager, such as [nvm](https://github.com/nvm-sh/nvm#intro). The [.nvmrc](/.nvmrc) file in the root directory of this repo will ensure the correct version is used once you run `nvm install`.

## Quick start

```bash
npm install
```

## Running DAG

### Step 0: Prerequisite Setup of Apps

- In the [Developer Portal](https://www.canva.com/developers/apps), create an app and assign the design read/write and asset read/write permissions. In the development URL: input `http://localhost:8080`
- After creating and assigning the URL and permissions, return to the developer portal and copy the App ID.
- In the .env file, paste in your id under CANVA_APP_ID

- Next, navigate to the [Integrations Portal](https://www.canva.com/developers/integrations/connect-api) and create a new integration. Copy the client ID into the .env file under CANVA_CLIENT_ID, then generate a client secret and in the .env file place it under CANVA_CLIENT_SECRET
- In the scopes tab, assign the following permissions: app read/write, asset read/write, design:content read/write, design:meta read, design:permission read/write
- In the authentication tab, paste in the following URL under URL1: `http://127.0.0.1:8000/api/v1/auth/oauth/redirect`

- We are almost done. Configure an AWS S3 account and create a new bucket, get an access key and access key secret from the IAM portal. The easiest option is to use the aws cli tool `aws configure` and set up authentication that way. Otherwise, some changes will need to be made to the backend code. Add the bucket name and region to the .env file under BUCKET_NAME and BUCKET_REGION

- Finally, get an OpenAI API Key, verify your organization identity, and save the key under OPENAI_API_KEY in the .env file.

The final .env file should look something like this:

```bash
CANVA_FRONTEND_PORT=8080
CANVA_BACKEND_PORT=3001
CANVA_BACKEND_HOST=http://localhost:3001 # TODO: replace this with your production URL before submitting your app
PYTHON_BACKEND=http://127.0.0.1:8000
CANVA_APP_ID=YOUR_APP_ID
CANVA_APP_ORIGIN=configuer under optional step
CANVA_HMR_ENABLED=
OPENAI_API_KEY=YOUR_OPENAI_KEY
CANVA_CLIENT_ID=YOUR_CLIENT_ID
CANVA_CLIENT_SECRET=YOUR_CLIENT_SECRET
REDIRECT_URI=http://127.0.0.1:8000/api/v1/auth/oauth/redirect
DATABASE_URL=sqlite:///app.db
BUCKET_NAME=YOUR_BUCKET_NAME
BUCKET_REGION=YOUR_BUCKET_REGION
```

### Step 1: Start the local development server

To start the boilerplate's development server, run the following command:

```bash
npm start
```

The server becomes available at <http://localhost:8080>.

In another terminal, navigate to the pythonbackend directory `cd backend/pythonbackend` and run the following:
`uv run -- fastapi dev src/main.py`

The app's source code is in the `src/app.tsx` file.

### Step 2: Preview the app

The local development server only exposes a JavaScript bundle, so you can't preview an app by visiting <http://localhost:8080>. You can only preview an app via the Canva editor.

To preview an app:

1. Create an app via the [Developer Portal](https://www.canva.com/developers/apps).
2. Select **App source > Development URL**.
3. In the **Development URL** field, enter the URL of the development server.
4. Click **Preview**. This opens the Canva editor (and the app) in a new tab.
5. Click **Open**. (This screen only appears when using an app for the first time.)

The app will appear in the side panel.

<details>
  <summary>Previewing apps in Safari</summary>

By default, the development server is not HTTPS-enabled. This is convenient, as there's no need for a security certificate, but it prevents apps from being previewed in Safari.

**Why Safari requires the development server to be HTTPS-enabled?**

Canva itself is served via HTTPS and most browsers prevent HTTPS pages from loading scripts via non-HTTPS connections. Chrome and Firefox make exceptions for local servers, such as `localhost`, but Safari does not, so if you're using Safari, the development server must be HTTPS-enabled.

To learn more, see [Loading mixed-content resources](https://developer.mozilla.org/en-US/docs/Web/Security/Mixed_content#loading_mixed-content_resources).

To preview apps in Safari:

1. Start the development server with HTTPS enabled:

```bash
npm start --use-https
```

2. Navigate to <https://localhost:8080>.
3. Bypass the invalid security certificate warning:
   1. Click **Show details**.
   2. Click **Visit website**.
4. In the Developer Portal, set the app's **Development URL** to <https://localhost:8080>.
5. Click preview (or refresh your app if it's already open).

You need to bypass the invalid security certificate warning every time you start the local server. A similar warning will appear in other browsers (and will need to be bypassed) whenever HTTPS is enabled.

</details>

### (Optional) Step 3: Enable Hot Module Replacement

By default, every time you make a change to an app, you have to reload the entire app to see the results of those changes. If you enable [Hot Module Replacement](https://webpack.js.org/concepts/hot-module-replacement/) (HMR), changes will be reflected without a full reload, which significantly speeds up the development loop.

**Note:** HMR does **not** work while running the development server in a Docker container.

To enable HMR:

1. Navigate to an app via the [Your apps](https://www.canva.com/developers/apps).
2. Select **Configure your app**.
3. Copy the value from the **App origin** field. This value is unique to each app and cannot be customized.
4. In the root directory, open the `.env` file.
5. Set the `CANVA_APP_ORIGIN` environment variable to the value copied from the **App origin** field:

   ```bash
   CANVA_APP_ORIGIN=# YOUR APP ORIGIN GOES HERE
   ```

6. Set the `CANVA_HMR_ENABLED` environment variable to `true`:

   ```bash
   CANVA_HMR_ENABLED=true
   ```

7. Restart the local development server.
8. Reload the app manually to ensure that HMR takes effect.

## Running an app's backend

Some templates provide an example backend. This backend is defined in the template's `backend/server.ts` file, automatically starts when the `npm start` command is run, and becomes available at <http://localhost:3001>.

To run templates that have a backend:

1. Navigate to the [Your apps](https://www.canva.com/developers/apps) page.
2. Copy the ID of an app from the **App ID** column.
3. In the starter kit's `.env` file, set `CANVA_APP_ID` to the ID of the app.

   For example:

   ```bash
   CANVA_APP_ID=AABBccddeeff
   CANVA_APP_ORIGIN=#
   CANVA_BACKEND_PORT=3001
   CANVA_FRONTEND_PORT=8080
   CANVA_BACKEND_HOST=http://localhost:3001
   CANVA_HMR_ENABLED=FALSE
   ```

4. Start the app:

   ```bash
   npm start
   ```

The ID of the app must be explicitly defined because it's required to [send and verify HTTP requests](https://www.canva.dev/docs/apps/verifying-http-requests/). If you don't set up the ID in the `.env` file, an error will be thrown when attempting to run the example.

## Customizing the backend host

If your app has a backend, the URL of the server likely depends on whether it's a development or production build. For example, during development, the backend is probably running on a localhost URL, but once the app's in production, the backend needs to be exposed to the internet.

To more easily customize the URL of the server:

1. Open the `.env` file in the text editor of your choice.
2. Set the `CANVA_BACKEND_HOST` environment variable to the URL of the server.
3. When sending a request, use `BACKEND_HOST` as the base URL:

   ```ts
   const response = await fetch(`${BACKEND_HOST}/custom-route`);
   ```

   **Note:** `BACKEND_HOST` is a global constant that contains the value of the `CANVA_BACKEND_HOST` environment variable. The variable is made available to the app via webpack and does not need to be imported.

4. Before bundling the app for production, update `CANVA_BACKEND_HOST` to point to the production backend.

## Configure ngrok (optional)

If your app requires authentication with a third party service, your server needs to be exposed via a publicly available URL, so that Canva can send requests to it.
This step explains how to do this with [ngrok](https://ngrok.com/).

**Note:** ngrok is a useful tool, but it has inherent security risks, such as someone figuring out the URL of your server and accessing proprietary information. Be mindful of the risks, and if you're working as part of an organization, talk to your IT department.
You must replace ngrok urls with hosted API endpoints for production apps.

To use ngrok, you'll need to do the following:

1. Sign up for a ngrok account at <https://ngrok.com/>.
2. Locate your ngrok [authtoken](https://dashboard.ngrok.com/get-started/your-authtoken).
3. Set an environment variable for your authtoken, using the command line. Replace `<YOUR_AUTH_TOKEN>` with your actual ngrok authtoken:

   For macOS and Linux:

   ```bash
   export NGROK_AUTHTOKEN=<YOUR_AUTH_TOKEN>
   ```

   For Windows PowerShell:

   ```shell
   $Env:NGROK_AUTHTOKEN = "<YOUR_AUTH_TOKEN>"
   ```

This environment variable is available for the current terminal session, so the command must be re-run for each new session. Alternatively, you can add the variable to your terminal's default parameters.

## Generative AI Template

This template captures best practices for improving user experience in your application.

### State Management

In this template, we've set up state management using `React Context`. It's just one way to do it, not a strict rule. If your app gets more complicated, you might want to check out other options like `Redux` or `MobX`.

### Routing

As your application evolves, you may find the need for routing to manage multiple views or pages. In this template, we've integrated React Router to illustrate how routing can facilitate seamless navigation between various components.

### Loading state

Creating AI assets can be time-consuming, often resulting in users facing extended waiting periods. Incorporating placeholders, a loading bar, and a message indicating the expected wait time can help alleviate the perceived wait time. We highly encourage adopting this approach and customizing it to suit your specific use case.

### Obscenity filter

In this template, we've included a basic obscenity filter to stop users from creating offensive or harmful content. However, you might need additional filters or checks after content generation to ensure it meets your standards.

### Backend

This template includes a simple Express server as a sample backend. Please note that this server is not production-ready, and we advise using it solely for instructional purposes to demonstrate API calls. If you require authentication for your app, we recommend looking at the authentication example provided in the [starter kit](https://github.com/canva-sdks/canva-apps-sdk-starter-kit).

### Thumbnails

This template illustrates how your API could return thumbnails and demonstrates their usage within the code. Thumbnails play a crucial role in optimizing image uploads and previews by providing quick visual feedback and reducing load times.

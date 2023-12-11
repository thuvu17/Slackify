# Spotify API
## Authorization Overview:
- Require API authorization to obtain an access token
- Use access token in API requests
- Spotify implement the OAuth 2.0 authorization framework:
    - End User corresponds to the Spotify user, who grants access to the protected resources (e.g. playlists, personal information, etc.)
    - Slackify is the client that requests access to the protected resources (e.g a mobile or web app)
    - Server which hosts the protected resources and provides authentication and authorization via OAuth 2.0.
## Getting Started:
- Login to the Spotify Developer Dashboard
- Create Slackify app in the Dashboard by clicking on the Create an app button and enter the following information:
    - App Name: Slackify App
    - App Description: (Brief description of what Slackify is)
    - Redirect URL: http://localhost:3000 (for local development at the moment)
- Slackify app needs to provide the Client ID and Client Secret needed to request an access token by implementing an authorization flow
- Request an access token:
    - Go to the Spotify Developer Dashboard
    - Click on the name Slackify
    - Click on the Settings button
    - Find Client ID and client Secret
        - Client Secret can be found behind the View client secret link
    - Use Client Credentials to:
        - Send a POST request to the token endpoint URL.
        - Add the Content-Type header set to the application/x-www-form-urlencoded value.
        - Add a HTTP body containing the Client ID and Client Secret, along with the grant_type parameter set to client_credentials.
        ```python
        curl -X POST "https://accounts.spotify.com/api/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
         -d "grant_type=client_credentials&client_id=your-client-id&client_secret=your-client-secret"
        ```
        The response will return an access token valid for 1 hour:
        ```python
        {
        "access_token": "BQDBKJ5eo5jxbtpWjVOj7ryS84khybFpP_lTqzV7uV-T_m0cTfwvdn5BnBSKPxKgEb11",
        "token_type": "Bearer",
        "expires_in": 3600
        }
        ```
## API Calls
- The Spotify Web API is a restful API with different endpoints which return JSON metadata about music artists, albums, and tracks, directly from the Spotify Data Catalogue.
- Base URL of the API is https://api.spotify.com
- Requests
| Method        | Action           
| ------------- |:-------------:
| GET           | Retrieves resources 
| POST          | Created resources     
| PUT           | Changes and/or replaces resources or collections
| DELETE        | Deletes resources     
- Response
    - Spotify API normally returns JSON in the response body
    - See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status for response codes

## API End-point for Slackify
- Get Track API 
    - Reference: https://developer.spotify.com/documentation/web-api/reference/get-track
    - TrackObject is important for our project's song data as it contains:
        - **name**: Name of the track
        - **popularity**: The popularity of the track. The value will be between 0 and 100, with 100 being the most popular.
        - **album**: String object of the album the track belongs to
        - **artists**: List of Artists involved in the track
        - **preview_url**: A link to a 30 second preview (MP3 format) of the track. Can be null
        - **uri**: The Spotify URI for the track.

- Get Tracks' Audio Features
    - Reference: https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features
- Save Tracks for Current User
    - Reference: https://developer.spotify.com/documentation/web-api/reference/save-tracks-user
- Get Recommendations
    - Reference: https://developer.spotify.com/documentation/web-api/reference/get-recommendations

    
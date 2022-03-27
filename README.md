# Yuna

A 24 hours Discord music / radio bot. Server playlist can be customized by members. Skip songs, shuffle, etc...

## Hosting Yourself

You can fork and host it yourself if you want since this is a private bot but you have to figure it out yourself a little. (I'm not bothered to give full-blown tutorial)

### Firebase Database

Create a Firebase container and setup firestore. Then create a collection called "guilds". Then create a service account and copy the account secrets.

### Environment Variables

Create an `.env` file in the root of the project and write this:

```sh
TOKEN='bot token goes here'
FIREBASE_CREDENTIALS='firebase admin sdk secrets (this gets parsed into JSON from string)'
```

### Done

Now just login into your bot and invite it to your servers. I don't recommend making it a public bot since hosting it use a lot of resources.

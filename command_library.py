def browser_open(query: str):
    import webbrowser

    conversion = {
        "youtube": "https://youtube.com",
        "messenger": "https://messenger.com",
        "yahoo finance": "https://finance.yahoo.com"
    }
    webbrowser.open_new(conversion[query])


def youtube_search(query: str):
    import pytube
    import webbrowser

    search = pytube.Search(query)
    first_video = search.results[0]
    webbrowser.open_new(first_video.watch_url)


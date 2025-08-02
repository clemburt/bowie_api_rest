# bowie_api_rest
A RESTful API built with FastAPI and SQLModel to explore David Bowie's discography

$ curl 'http://127.0.0.1:8000/tracks/Fa/albums'
[{"title":"Diamond Dogs","year":1974,"id":7,"tracks":[{"title":"Chant of the Ever Circling Skeletal Family","duration":"4:46","id":76}]},{"title":"Young Americans","year":1975,"id":8,"tracks":[{"title":"Fascination","duration":"3:43","id":79},{"title":"Fame","duration":"4:12","id":83}]},{"title":"Lodger","year":1979,"id":12,"tracks":[{"title":"Fantastic Voyage","duration":"2:55","id":112}]},{"title":"Scary Monsters (and Super Creeps)","year":1980,"id":13,"tracks":[{"title":"Fashion","duration":"4:48","id":126}]}]


$ curl 'http://127.0.0.1:8000/tracks/Fashion/albums'
[{"title":"Scary Monsters (and Super Creeps)","year":1980,"id":13,"tracks":[{"title":"Fashion","duration":"4:48","id":126}]}]

$ curl -G "http://127.0.0.1:8000/albums/by-title/" --data-urlencode "album_title=scary monsters"
{"title":"Scary Monsters (and Super Creeps)","year":1980,"id":13,"tracks":[{"title":"It's No Game (No. 1)","duration":"4:20","id":122},{"title":"Up the Hill Backwards","duration":"2:43","id":123},{"title":"Scary Monsters (and Super Creeps)","duration":"4:08","id":124},{"title":"Ashes to Ashes","duration":"4:26","id":125},{"title":"Fashion","duration":"4:48","id":126},{"title":"Teenage Wildlife","duration":"6:51","id":127},{"title":"Scream Like a Baby","duration":"3:36","id":128},{"title":"Kingdom Come","duration":"2:49","id":129},{"title":"Because You're Young","duration":"2:50","id":130},{"title":"Crossfire","duration":"5:34","id":131},{"title":"You're Not Alone","duration":"2:45","id":132},{"title":"Future Legend","duration":"0:55","id":133},{"title":"Teenage Wildlife (Reprise)","duration":"1:18","id":134}]}

$ uvicorn bowie_api_rest.main:app --reload
INFO:     Will watch for changes in these directories: ['/home/clement.burtscher/tools/clement/bowie_api_rest/bowie_api_rest']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [1479268] using StatReload
INFO:     Started server process [1479270]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


pdm run find-track "Fa"

pdm run find-album "scary monsters (and super creeps)"
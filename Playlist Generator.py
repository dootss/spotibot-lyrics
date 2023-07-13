import spotipy
import spotipy.util as util
import re
sentence = re.sub('[!.,"?()]','',str(input('Sentence to create a playlist from? '))) #replaces ! . , " ? with nothing as i've seen the program have trouble with them before
#sentence = re.sub('[-]',' ',sentence)
print(sentence)


converted_sentence = sentence.lower().split()

print(converted_sentence)
results = []
song_ids = []


title = str(input('Enter a title for your playlist. '))



def start():
    sp.trace = False

    for word in converted_sentence:
        search(word)
    generate_playlist()


def search(word):
    song_names = set()
    i = -1
    while len(song_names) == 0 or word.lower() not in song_names:
        i += 1
        if i <= 15:
            #print(i)
            results = sp.search(word, limit=50, offset=i*50, type='track', market=None)
            for item in results['tracks']['items']:
                song_names.add(item['name'].lower())
            #print(song_names)
        else: # splitting if searched 750 results, otherwise it'll just hit the max searches and end
            split = list(word)
            for letter in split:
                search(letter)
            break

    for item in results['tracks']['items']:
        if item['name'].lower() == word:
            song_ids.append(item["id"])
            #print(song_ids)
            print(word)
            break


        

def generate_playlist():
    playlist = sp.user_playlist_create(username, title, public=True, collaborative=False, description="made by dootw's playlist bot! https://github.com/dootss/spotibot-lyrics")
    playlist_id = playlist["id"]
    print(playlist_id)
    for id in song_ids:
        sp.playlist_add_items(playlist_id, [id])


# SECTION FOR PASTING IDS #
if __name__ == '__main__':
    scope = 'playlist-modify-public'
    username = '' # your spotify id
    client_id = '' # your apps id
    client_secret = '' # your apps secret
    redirect_url = 'http://localhost:8080'


    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret,redirect_uri=redirect_url)

    if token:
        sp = spotipy.Spotify(auth=token)
        start()
    else:
        print('Cant get token for', username)

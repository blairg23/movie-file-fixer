import json

poorly_formed = {"Title":"A Gun, a Car, a Blonde","Year":"1997","Rated":"UNRATED","Released":"01 Jun 1997","Runtime":"107 min","Genre":"Drama, Thriller","Director":"Stefani Ames","Writer":"Tom Epperson, Stefani Ames","Actors":"Jim Metzler, Victor Love, Kay Lenz, Norma Maldonado","Plot":"The story's hero (played by Jim Metzler) has lost much of his spine and the love of his life, due to cancer. He's in remission; but decimated in body, shattered in mind, and separated from inner\spiritual peace. Richard uses \"object therapy\" suggested by his lifelong pal (John Ritter)to project his consciousness into an alternative reality, where he becomes \"Rick Stone\" - a soft-hearted, tough acting, Private Dick (P.I.) It is here that he works through his existential fight to survive and transcend life.","Language":"English","Country":"USA","Awards":"1 win.","Poster":"N/A","Metascore":"N/A","imdbRating":"5.4","imdbVotes":"258","imdbID":"tt0120690","Type":"movie","Response":"True"}

special_chars = ['\b', '\f', '\n', '\r', '\t', '\"', '\\']


with open('data.json', 'w') as fp:
     json.dump(poorly_formed, fp)
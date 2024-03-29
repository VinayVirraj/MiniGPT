#parameters
import torch.nn as nn
from torch.nn import functional as F
import torch
from tokenizers import Tokenizer
from utils import nanoGPT

import json
with open('tokenizer/char_to_index.json','r') as f:
  char_to_index = json.load(f)
with open('tokenizer/index_to_char.json','r') as f:
  index_to_char = json.load(f)

encode = lambda seq: [char_to_index[i] for i in seq]
decode = lambda seq: [index_to_char[str(i)] for i in seq]
# encoded = tokenizer.encode("I can feel the magic, can you?")




#parameters
block_size = 512
batch_size = 64
device = 'cuda' if torch.cuda.is_available() else 'cpu'
eval_iters = 200
N = 6
d_model = 512
n_heads = 8
vocab_size = len(char_to_index)#25000#tokenizer.get_vocab_size()
d_ff = 2048
learning_rate = 3e-4
max_iters = 7000
eval_interval = 500

gpt = nanoGPT(d_model, n_heads, d_ff, vocab_size, block_size, N)

gpt = gpt.to(device)
PATH = 'model/nanoGPT_char_5008.pt'
gpt.load_state_dict(torch.load(PATH, map_location=device))

import streamlit as st

artist_list = ['ABBA',
 'Ace Of Base',
 'Adam Sandler',
 'Adele',
 'Aerosmith',
 'Air Supply',
 'Aiza Seguerra',
 'Alabama',
 'Alan Parsons Project',
 'Aled Jones',
 'Alice Cooper',
 'Alice In Chains',
 'Alison Krauss',
 'Allman Brothers Band',
 'Alphaville',
 'America',
 'Amy Grant',
 'Andrea Bocelli',
 'Andy Williams',
 'Annie',
 'Ariana Grande',
 'Ariel Rivera',
 'Arlo Guthrie',
 'Arrogant Worms',
 'Avril Lavigne',
 'Backstreet Boys',
 'Barbie',
 'Barbra Streisand',
 'Beach Boys',
 'The Beatles',
 'Beautiful South',
 'Beauty And The Beast',
 'Bee Gees',
 'Bette Midler',
 'Bill Withers',
 'Billie Holiday',
 'Billy Joel',
 'Bing Crosby',
 'Black Sabbath',
 'Blur',
 'Bob Dylan',
 'Bob Marley',
 'Bob Rivers',
 'Bob Seger',
 'Bon Jovi',
 'Boney M.',
 'Bonnie Raitt',
 'Bosson',
 'Bread',
 'Britney Spears',
 'Bruce Springsteen',
 'Bruno Mars',
 'Bryan White',
 'Cake',
 'Carly Simon',
 'Carol Banawa',
 'Carpenters',
 'Cat Stevens',
 'Celine Dion',
 'Chaka Khan',
 'Cheap Trick',
 'Cher',
 'Chicago',
 'Children',
 'Chris Brown',
 'Chris Rea',
 'Christina Aguilera',
 'Christina Perri',
 'Christmas Songs',
 'Christy Moore',
 'Chuck Berry',
 'Cinderella',
 'Clash',
 'Cliff Richard',
 'Coldplay',
 'Cole Porter',
 'Conway Twitty',
 'Counting Crows',
 'Creedence Clearwater Revival',
 'Crowded House',
 'Culture Club',
 'Cyndi Lauper',
 'Dan Fogelberg',
 'Dave Matthews Band',
 'David Allan Coe',
 'David Bowie',
 'David Guetta',
 'David Pomeranz',
 'Dean Martin',
 'Death',
 'Deep Purple',
 'Def Leppard',
 'Demi Lovato',
 'Depeche Mode',
 'Devo',
 'Dewa 19',
 'Diana Ross',
 'Dire Straits',
 'Divine',
 'Dolly Parton',
 'Don Henley',
 'Don McLean',
 'Don Moen',
 'Donna Summer',
 'Doobie Brothers',
 'Doors',
 'Doris Day',
 'Drake',
 'Dream Theater',
 'Dusty Springfield',
 'Eagles',
 'Ed Sheeran',
 'Eddie Cochran',
 'Electric Light Orchestra',
 'Ella Fitzgerald',
 'Ellie Goulding',
 'Elton John',
 'Elvis Costello',
 'Elvis Presley',
 'Eminem',
 'Emmylou Harris',
 'Engelbert Humperdinck',
 'Enigma',
 'Enrique Iglesias',
 'Enya',
 'Eppu Normaali',
 'Erasure',
 'Eric Clapton',
 'Erik Santos',
 'Etta James',
 'Europe',
 'Eurythmics',
 'Evanescence',
 'Everclear',
 'Everlast',
 'Exo',
 'Exo-K',
 'Extreme',
 'Fabolous',
 'Face To Face',
 'Faces',
 'Faith Hill',
 'Faith No More',
 'Falco',
 'Fall Out Boy',
 'Fastball',
 'Fatboy Slim',
 'Fifth Harmony',
 'Fiona Apple',
 'Fleetwood Mac',
 'Flo-Rida',
 'Foo Fighters',
 'Foreigner',
 'Frank Sinatra',
 'Frank Zappa',
 'Frankie Goes To Hollywood',
 'Frankie Laine',
 'Frankie Valli',
 'Freddie Aguilar',
 'Freddie King',
 'Free',
 'Freestyle',
 'Fun.',
 'Garth Brooks',
 'Gary Numan',
 'Gary Valenciano',
 'Genesis',
 'George Formby',
 'George Harrison',
 'George Jones',
 'George Michael',
 'George Strait',
 'Gino Vannelli',
 'Gipsy Kings',
 'Glee',
 'Glen Campbell',
 'Gloria Estefan',
 'Gloria Gaynor',
 'GMB',
 'Gordon Lightfoot',
 'Grand Funk Railroad',
 'Grateful Dead',
 'Grease',
 'Great Big Sea',
 'Green Day',
 'Gucci Mane',
 'Guided By Voices',
 "Guns N' Roses",
 'Halloween',
 'Hank Snow',
 'Hank Williams',
 'Hank Williams Jr.',
 'Hanson',
 'Happy Mondays',
 'Harry Belafonte',
 'Harry Connick, Jr.',
 'Heart',
 'Helloween',
 'High School Musical',
 'Hillsong',
 'Hillsong United',
 'HIM',
 'Hollies',
 'Hooverphonic',
 'Horrible Histories',
 'Housemartins',
 'Howard Jones',
 'Human League',
 'Ian Hunter',
 'Ice Cube',
 'Idina Menzel',
 'Iggy Pop',
 'Il Divo',
 'Imagine Dragons',
 'Imago',
 'Imperials',
 'Incognito',
 'Incubus',
 'Independence Day',
 'Indiana Bible College',
 'Indigo Girls',
 'Ingrid Michaelson',
 'Inna',
 'Insane Clown Posse',
 'Inside Out',
 'INXS',
 'Iron Butterfly',
 'Iron Maiden',
 'Irving Berlin',
 'Isley Brothers',
 'Israel',
 'Israel Houghton',
 'Iwan Fals',
 'J Cole',
 'Jackson Browne',
 'The Jam',
 'James Taylor',
 'Janis Joplin',
 'Jason Mraz',
 'Jennifer Lopez',
 'Jim Croce',
 'Jimi Hendrix',
 'Jimmy Buffett',
 'John Denver',
 'John Legend',
 'John Martyn',
 'John McDermott',
 'John Mellencamp',
 'John Prine',
 'John Waite',
 'Johnny Cash',
 'Joni Mitchell',
 'Jose Mari Chan',
 'Josh Groban',
 'Journey',
 'Joy Division',
 'Judas Priest',
 'Judds',
 'Judy Garland',
 'Justin Bieber',
 'Justin Timberlake',
 'Kanye West',
 'Kari Jobe',
 'Kate Bush',
 'Katy Perry',
 'Keith Green',
 'Keith Urban',
 'Kelly Clarkson',
 'Kelly Family',
 'Kenny Chesney',
 'Kenny Loggins',
 'Kenny Rogers',
 'Kid Rock',
 'The Killers',
 'Kim Wilde',
 'King Crimson',
 'King Diamond',
 'Kinks',
 'Kirk Franklin',
 'Kirsty Maccoll',
 'Kiss',
 'Koes Plus',
 'Korn',
 'Kris Kristofferson',
 'Kyla',
 'Kylie Minogue',
 'Lady Gaga',
 'Lana Del Rey',
 'Lata Mangeshkar',
 'Lauryn Hill',
 'Lea Salonga',
 'Leann Rimes',
 'Lenny Kravitz',
 'Leo Sayer',
 'Leonard Cohen',
 'Les Miserables',
 'Lil Wayne',
 'Linda Ronstadt',
 'Linkin Park',
 'Lionel Richie',
 'Little Mix',
 'Little Walter',
 'LL Cool J',
 'Lloyd Cole',
 'Lorde',
 'Loretta Lynn',
 'Lou Reed',
 'Louis Armstrong',
 'Louis Jordan',
 'Lucky Dube',
 'Luther Vandross',
 'Lynyrd Skynyrd',
 'Madonna',
 'Manowar',
 'Mariah Carey',
 'Marianne Faithfull',
 'Marillion',
 'Marilyn Manson',
 'Mark Ronson',
 'Maroon 5',
 'Mary Black',
 'Matt Monro',
 'Matt Redman',
 'Mazzy Star',
 'Mc Hammer',
 'Meat Loaf',
 'Megadeth',
 'Men At Work',
 'Metallica',
 'Michael Bolton',
 'Michael Buble',
 'Michael Jackson',
 'Michael W. Smith',
 'Migos',
 'Miley Cyrus',
 'Misfits',
 'Modern Talking',
 'The Monkees',
 'Moody Blues',
 'Morrissey',
 'Mud',
 "'n Sync",
 'Nat King Cole',
 'Natalie Cole',
 'Natalie Grant',
 'Natalie Imbruglia',
 'Nazareth',
 'Ne-Yo',
 'Neil Diamond',
 'Neil Sedaka',
 'Neil Young',
 'New Order',
 'Next To Normal',
 'Nick Cave',
 'Nick Drake',
 'Nickelback',
 'Nicki Minaj',
 'Nightwish',
 'Nina Simone',
 'Nine Inch Nails',
 'Nirvana',
 'Nitty Gritty Dirt Band',
 'Noa',
 'NOFX',
 'Norah Jones',
 'Notorious B.I.G.',
 'O-Zone',
 'O.A.R.',
 'Oasis',
 'Ocean Colour Scene',
 'Offspring',
 'Ofra Haza',
 'Oingo Boingo',
 "Old 97's",
 'Oliver',
 'Olivia Newton-John',
 'Olly Murs',
 'Omd',
 'One Direction',
 'OneRepublic',
 'Opeth',
 'Orphaned Land',
 'Oscar Hammerstein',
 'Otis Redding',
 'Our Lady Peace',
 'Out Of Eden',
 'Outkast',
 'Overkill',
 'Owl City',
 'Ozzy Osbourne',
 'Passenger',
 'Pat Benatar',
 'Patsy Cline',
 'Patti Smith',
 'Paul McCartney',
 'Paul Simon',
 'Pearl Jam',
 'Perry Como',
 'Pet Shop Boys',
 'Peter Cetera',
 'Peter Gabriel',
 'Peter Tosh',
 'Pharrell Williams',
 'Phil Collins',
 'Phineas And Ferb',
 'Phish',
 'Pink Floyd',
 'Pitbull',
 'Planetshakers',
 'P!nk',
 'Pogues',
 'Point Of Grace',
 'Poison',
 'Pretenders',
 'Primus',
 'Prince',
 'Proclaimers',
 'Procol Harum',
 'Puff Daddy',
 'Q-Tip',
 'Qntal',
 'Quarashi',
 'Quarterflash',
 'Quasi',
 'Queen',
 'Queen Adreena',
 'Queen Latifah',
 'Queens Of The Stone Age',
 'Queensryche',
 'Quicksand',
 'Quicksilver Messenger Service',
 'Quiet Riot',
 'Quietdrive',
 'Quincy Jones',
 'Quincy Punx',
 'R. Kelly',
 'Radiohead',
 'Raffi',
 'Rage Against The Machine',
 'Rainbow',
 'Rammstein',
 'Ramones',
 'Randy Travis',
 'Rascal Flatts',
 'Ray Boltz',
 'Ray Charles',
 'Reba Mcentire',
 'Red Hot Chili Peppers',
 'Regine Velasquez',
 'Religious Music',
 'Rem',
 'Reo Speedwagon',
 'Richard Marx',
 'Rick Astley',
 'Rihanna',
 'Robbie Williams',
 'Rod Stewart',
 'Rolling Stones',
 'Roxette',
 'Roxy Music',
 'Roy Orbison',
 'Rush',
 'Sam Smith',
 'Santana',
 'Savage Garden',
 'Scorpions',
 'Selah',
 'Selena Gomez',
 'Sia',
 'Side A',
 'Slayer',
 'Smiths',
 'Snoop Dogg',
 'Soundgarden',
 'Spandau Ballet',
 'Squeeze',
 'Starship',
 'Status Quo',
 'Steely Dan',
 'Steve Miller Band',
 'Stevie Ray Vaughan',
 'Stevie Wonder',
 'Sting',
 'Stone Roses',
 'Stone Temple Pilots',
 'Styx',
 'Sublime',
 'Supertramp',
 'System Of A Down',
 'Talking Heads',
 'Taylor Swift',
 'Tears For Fears',
 'The Temptations',
 'Ten Years After',
 'The Broadways',
 'The Script',
 'The Weeknd',
 'Thin Lizzy',
 'Tiffany',
 'Tim Buckley',
 'Tim McGraw',
 'Tina Turner',
 'Tom Jones',
 'Tom Lehrer',
 'Tom T. Hall',
 'Tom Waits',
 'Tool',
 'Tori Amos',
 'Toto',
 'Townes Van Zandt',
 'Tracy Chapman',
 'Tragically Hip',
 'Train',
 'Travis',
 'Twenty One Pilots',
 'U. D. O.',
 'U-Kiss',
 'U2',
 'UB40',
 'Ufo',
 'Ugly Kid Joe',
 "Ultramagnetic Mc's",
 'Ultravox',
 'Uncle Kracker',
 'Uncle Tupelo',
 'Underoath',
 'Underworld',
 'Unearth',
 'Ungu',
 'Unkle',
 'Unknown',
 'Unseen',
 'Unwritten Law',
 'Uriah Heep',
 'Used',
 'Usher',
 'Utada Hikaru',
 'Utopia',
 'Van Halen',
 'Van Morrison',
 'Vanessa Williams',
 'Vangelis',
 'Vanilla Ice',
 'Velvet Underground',
 'Vengaboys',
 'Venom',
 'Vera Lynn',
 'Vertical Horizon',
 'Veruca Salt',
 'Verve',
 'Vince Gill',
 'Violent Femmes',
 'Virgin Steele',
 'Vonda Shepard',
 'Vybz Kartel',
 'Walk The Moon',
 'Wanda Jackson',
 'Wang Chung',
 'Warren Zevon',
 'W.A.S.P.',
 'Waterboys',
 'Waylon Jennings',
 'Ween',
 'Weezer',
 'Weird Al Yankovic',
 'Westlife',
 'Wet Wet Wet',
 'Wham!',
 'Whiskeytown',
 'The White Stripes',
 'Whitesnake',
 'Whitney Houston',
 'Who',
 'Widespread Panic',
 'Will Smith',
 'Willie Nelson',
 'Wilson Phillips',
 'Wilson Pickett',
 'Wishbone Ash',
 'Within Temptation',
 'Wiz Khalifa',
 'Wu-Tang Clan',
 'Wyclef Jean',
 'X',
 'X Japan',
 'X-Raided',
 'X-Ray Spex',
 'X-Treme',
 'Xandria',
 'Xavier Naidoo',
 'Xavier Rudd',
 'Xentrix',
 'Xiu Xiu',
 'Xscape',
 'XTC',
 'Xzibit',
 'Yazoo',
 'Yeah Yeah Yeahs',
 'Yelawolf',
 'Yello',
 'Yellowcard',
 'Yeng Constantino',
 'Yes',
 'YG',
 'Ying Yang Twins',
 'Yngwie Malmsteen',
 'Yo Gotti',
 'Yo La Tengo',
 'Yoko Ono',
 'Yolanda Adams',
 'Yonder Mountain String Band',
 'You Am I',
 'Young Buck',
 'Young Dro',
 'Young Jeezy',
 'Youngbloodz',
 'Youth Of Today',
 'Yukmouth',
 'Yung Joc',
 'Yusuf Islam',
 'Z-Ro',
 'Zac Brown Band',
 'Zakk Wylde',
 'Zao',
 'Zayn Malik',
 'Zebra',
 'Zebrahead',
 'Zed',
 'Zero 7',
 'Zeromancer',
 'Ziggy Marley',
 'Zoe',
 'Zoegirl',
 'Zornik',
 'Zox',
 'Zucchero',
 'Zwan',
 'ZZ Top',
 'Joseph And The Amazing Technicolor Dreamcoat',
 'Soundtracks',
 'Van Der Graaf Generator',
 'Various Artists',
 'Zazie']
from utils import generate

def main():
    st.set_page_config(page_title="SongGPT")
    st.header("Generate Your Own Song")

    artist = st.selectbox("Select Artist", artist_list)
    song_start = st.text_input("Give a short start to the song")
    if song_start != '':
        input = f"<artist> {artist}\n<lyrics> {song_start}"
        # print(encode(input))
        context = torch.tensor(encode(input), dtype=torch.long, device=device)
        context = context.unsqueeze(0)
        idxs = generate(gpt,context, 1000)
        st.text(idxs.split('<lyrics>')[1])
        # st.write(encode(input))

if __name__ == '__main__':
    main()

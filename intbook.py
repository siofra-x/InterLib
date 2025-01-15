import sqlite3

def intbook_db():
        conn = sqlite3.connect('intbook.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
            BookId INTEGER PRIMARY KEY AUTOINCREMENT,
            GenreId INT NOT NULL,
            CurrencyId INT NOT NULL,
            Price INT NOT NULL,
            Title CHAR(200) NOT NULL,
            Author CHAR(200) NOT NULL,
            Series_name CHAR(200),
            ISBN INT NOT NULL,
            Country CHAR(200) NOT NULL,
            Language CHAR(200) NOT NULL,
            Blurb CHAR(200) NOT NULL,
            Cover_url CHAR(300) NOT NULL,
            FOREIGN KEY (GenreId) REFERENCES Genre(GenreId),
            FOREIGN KEY (CurrencyId) REFERENCES Currency(CurrencyId)
            )
            ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Genre (
                GenreId INTEGER PRIMARY KEY AUTOINCREMENT,
                Type CHAR(50) NOT NULL
            )
            ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
            UserId INTEGER PRIMARY KEY AUTOINCREMENT,
            Username VARCHAR(50) NOT NULL,
            Password VARCHAR(50) NOT NULL,
            Email CHAR(50) NOT NULL,
            Origin_country CHAR(50) NOT NULL
            )
            ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Currency (
                CurrencyId INTEGER PRIMARY KEY AUTOINCREMENT,
                Currency_type CHAR(50) NOT NULL,
                Symbol VARCHAR(1) NOT NULL
            )
            ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Favourites (
            UserId INT NOT NULL,
            BookId INT NOT NULL,
            FOREIGN KEY (UserId) REFERENCES Users(UserId),
            FOREIGN KEY (BookId) REFERENCES Books(BookId)
            )
            ''')

        cursor.execute('''INSERT INTO Genre(GenreId, Type)
        VALUES
        (1, "Fiction"),
        (2, "Non-fiction"),
        (3, "Fantasy"),
        (4, "Science Fiction"),
        (5, "Romance"),
        (6, "Horror"),
        (7, "Thriller"),
        (8, "Historical"),
        (9, "Mystery/Crime"),
        (10, "Adventure/Action"),
        (11, "Poetry"),
        (12, "Drama"),
        (13, "Literature");
        ''')

        cursor.execute('''INSERT INTO Currency(CurrencyId, Currency_type, Symbol)
        VALUES
        (1, "Euro", "€"),
        (2, "US Dollar", "$"),
        (3, "Pound Sterling", "£"),
        (4, "Chinese Yuan", "¥");
        ''')

        cursor.execute('''INSERT INTO Books(BookId, GenreId, CurrencyId, Price, Title, Author, Series_name, ISBN, Country, Language, Blurb, Cover_url)
        VALUES
        (1, 3, 1, 11.50, "A Court of Thorns and Roses", "Sarah J. Maas", "A Court of Thorns and Roses", 9781635575569, "USA", "English",
        "When nineteen-year-old huntress Feyre kills a wolf in the woods, a terrifying creature arrives to demand retribution. Dragged to a treacherous magical land she knows about only from legends, Feyre discovers that her captor is not truly a beast, but one of the lethal, immortal faeries who once ruled her world.
        At least, he’s not a beast all the time. As she adapts to her new home, her feelings for the faerie, Tamlin, transform from icy hostility into a fiery passion that burns through every lie she’s been told about the beautiful, dangerous world of the Fae. But something is not right in the faerie lands. An ancient, wicked shadow is growing, and Feyre must find a way to stop it, or doom Tamlin—and his world—forever.",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1620324329i/50659467.jpg"),

        (2, 3, 1, 18.99, "Hof van Doorns en Rozen", "Sarah J. Maas", "Hof van Doorns en Rozen", 9789000374373, "USA", "Dutch",
        "Het bos waarin de negentienjarige Feyre woont is in de lange wintermaanden een koude, sombere plek. Haar overlevingskansen en die van haar familie berusten op haar vermogen om te jagen. Wanneer ze een hert ziet dat opgejaagd wordt door een wolf kan ze de verleiding niet weerstaan om te vechten voor de prooi. Maar om te winnen moet ze de wolf doden en daarop staat een prijs. Niet veel later verschijnt er een beestachtig wezen om vergelding op te eisen. Wanneer ze naar het gevreesde feeënrijk Prythian wordt gesleept, ontdekt Feyre dat haar ontvoerder geen beest is, maar Tamlin – een van de dodelijkste, onsterfelijke magische wezens ooit gekend.
        Terwijl ze op zijn landgoed verblijft, veranderen haar ijzige vijandige gevoelens voor Tamlin in een vurige passie die elke leugen en waarschuwing over de mooie, gevaarlijke wereld van de Elfiden in rook doet opgaan. Maar een oude, kwaadaardige schaduw groeit over het land, en Feyre moet een manier vinden om het te stoppen of Tamlin en zijn wereld zullen voor eeuwig verdoemd zijn.",
        "https://api.bruna.nl/images/active/carrousel/fullsize/9789000374373_front.jpg");
        ''')

        cursor.execute('''INSERT INTO Users(UserId, Username, Password, Email, Origin_country)
        VALUES
        (1, "Admin", "AministratorRulez0303!", "sofiacrainic19@gmail.com", "Romania");
        ''')

        cursor.execute('''INSERT INTO Favourites(UserId, BookId)
        VALUES
        (1, 1);
        ''')

        conn.commit()
        conn.close()

if __name__ == "__main__":
    intbook_db()



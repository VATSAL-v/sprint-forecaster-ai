st.subheader("Plan a New Feature")

# 1. The Complete YinzCam Tricode Directory
YINZCAM_TRICODES = [
    "ABADBC", # Dubai Basketball
    "AHLCLE", # Cleveland Monsters
    "AHLLV", # Lehigh Valley Phantoms
    "CFLCGY", # Calgary Stampeders
    "CFLSSK", # Saskatchewan Roughriders
    "CFLTOR", # Toronto Argonauts
    "CFLWPG", # Winnipeg Blue Bombers
    "COMMVBR", # Verizon Basking Ridge
    "F1LV", # Formula 1-LV
    "F1PC", # Paddock Club
    "F1SS", # Silverstone Circuit
    "FABAR", # Barnsley F.C.
    "FABHA", # Brighton & Hove Albion
    "FABIR", # Birmingham FC
    "FABLB", # Blackburn Rovers F.C.
    "FABRE", # Brentford FC
    "FABUR", # Burnley FC
    "FACEF", # Celtic FC
    "FALEE", # Leeds United FC
    "FALEI", # Leicester City FC
    "FASUN", # Sunderland A.F.C.
    "FATOT", # Tottenham Hotspur
    "FAWOL", # Wolverhampton Wanderers F.C.
    "IOCCAN", # Team Canada
    "MFFLEAGUE", # Liga MX
    "MFFMNT", # Rayados
    "MFFNATIONAL", # Mexico National Team
    "MLSATL", # Atlanta United
    "MLSATX", # Austin FC
    "MLSCHI", # Chicago Fire
    "MLSCIN", # FC Cincinnati
    "MLSCLB", # Columbus Crew SC App
    "MLSCLT", # Charlotte FC
    "MLSCOL", # Colorado Rapids
    "MLSDC", # D.C. United
    "MLSHCF", # Huntsville City FC
    "MLSHOU", # Dynamo FC
    "MLSLA", # LA Galaxy
    "MLSLAFC", # Los Angeles FC
    "MLSMIN", # Minnesota United
    "MLSNSH", # Nashville SC
    "MLSNYCFC", # New York City FC
    "MLSPHI", # Philadelphia Union
    "MLSRBNY", # New York Red Bulls
    "MLSRSL", # Real Salt Lake
    "MLSSD", # San Diego FC
    "MLSSEA", # Seattle Sounders
    "MLSSKC", # Sporting KC
    "MLSSKCTV", # Sporting KC TV
    "MLSTOR", # Toronto FC Mobile
    "NBADCTN", # Canton Charge
    "NBADDEL", # Delaware Blue Coats
    "NBADSBL", # South Bay Lakers
    "NBADSCW", # Santa Cruz Warriors
    "NBABKN", # Brooklyn Nets
    "NBABOS", # Boston Celtics
    "NBACHA", # Charlotte Hornets
    "NBACLE", # Cleveland Cavaliers
    "NBADEN", # Denver Nuggets
    "NBAHOU", # Houston Rockets
    "NBALAC", # LA Clippers
    "NBALAL", # Los Angeles Lakers
    "NBAMIL", # Milwaukee Bucks
    "NBAMIN", # Minnesota Timberwolves
    "NBANOP", # New Orleans Pelicans
    "NBANYK", # New York Knicks
    "NBAOKC", # Oklahoma City Thunder
    "NBAOKCTV", # OKC Thunder TV
    "NBAORL", # Orlando Magic
    "NBAPHI", # Philadelphia 76ers
    "NBAPHX", # Phoenix Suns
    "NBAPOR", # Portland Trail Blazers
    "NBASAC", # Sacramento Kings
    "NBATOR", # Raptors Mobile
    "NBAUTA", # Utah Jazz
    "NBAWAS", # Washington Wizards Mobile
    "NCAATXAM", # Texas A&M Athletics
    "NFLARI", # Arizona Cardinals
    "NFLATLFB", # Flowery Branch
    "NFLATLMBS", # Mercedes Benz Stadium
    "NFLBAL", # Baltimore Ravens
    "NFLBALTV", # Ravens Mobile TV
    "NFLBUF", # Buffalo Bills
    "NFLCAR", # Carolina Panthers
    "NFLCHI", # Chicago Bears
    "NFLCIN", # Cincinnati Bengals
    "NFLCLE", # Cleveland Browns
    "NFLDAL", # Dallas Cowboys
    "NFLDALTV", # Dallas Cowboys TV
    "NFLDEN", # Denver Broncos
    "NFLDET", # Detroit Lions
    "NFLGB", # Green Bay Packers
    "NFLGBTV", # Green Bay Packers TV
    "NFLKC", # Kansas City Chiefs
    "NFLLAC", # Los Angeles Chargers
    "NFLLV", # Las Vegas Raiders (INTERNAL)
    "NFLMIA", # Miami Dolphins
    "NFLMIN", # Minnesota Vikings
    "NFLNO", # New Orleans Saints
    "NFLNYG", # New York Giants
    "NFLNYGTV", # New York Giants TV
    "NFLNYJ", # New York Jets
    "NFLOAK", # Las Vegas Raiders
    "NFLPHI", # Philadelphia Eagles
    "NFLPIT", # Pittsburgh Steelers
    "NFLSEA", # Seattle Seahawks
    "NFLSF", # San Francisco 49ers
    "NFLTB", # Tampa Bay Buccaneers
    "NFLTEN", # Tennessee Titans
    "NFLWAS", # Washington Commanders
    "NHLANA", # Anaheim Ducks Mobile
    "NHLARI", # Arizona Coyotes Mobile
    "NHLBOS", # Boston Bruins
    "NHLBUF", # Buffalo Sabres
    "NHLCAR", # Carolina Hurricanes
    "NHLCBJ", # Columbus Blue Jackets
    "NHLCHI", # Chicago Blackhawks
    "NHLCOL", # Colorado Avalanche
    "NHLDAL", # Dallas Stars
    "NHLDET", # Detroit Red Wings Mobile
    "NHLFLA", # Florida Panthers
    "NHLLAK", # Los Angeles Kings Mobile
    "NHLMIN", # Minnesota Wild
    "NHLNJD", # New Jersey Devils
    "NHLNJDTV", # New Jersey Devils TV
    "NHLNSH", # Nashville Predators Mobile
    "NHLNYI", # New York Islanders
    "NHLOTT", # Ottawa Senators
    "NHLPIT", # Penguins Mobile
    "NHLSJS", # San Jose Sharks
    "NHLSTL", # St. Louis Blues Mobile
    "NHLTBL", # Tampa Bay Lightning
    "NHLTOR", # Leafs Mobile
    "NHLUTA", # Utah Mammoth
    "NHLVGK", # Vegas Golden Knights
    "NWSLBAY", # Bay FC
    "NWSLHOU", # Dash
    "NWSLKC", # Kansas City Current
    "NWSLLA", # Angel City FC
    "NWSLSEA", # Seattle Reign FC
    "NWSLUTA", # Utah Royals
    "PJLLEAGUE", # Premier Jumping League
    "SFARAN", # Rangers
    "TENCAO", # Canadian Open
    "TENIWTG", # Indian Wells Tennis Garden
    "TENMIA", # Miami Open
    "TENWS", # Western & Southern Open Android
    "TENWSO", # Western & Southern Open
    "VENUEAAC", # American Airlines Center
    "VENUEACR", # Acrisure Stadium
    "VENUEAKC", # American Kennel Club
    "VENUEAMALIE", # Amalie Arena
    "VENUEANA", # Honda Center
    "VENUEAP", # Altitude Presents
    "VENUEAUD", # Audi Field
    "VENUEBAA", # British Airways Olympia Venue
    "VENUEBC", # Barclays Center
    "VENUEBHA", # American Express Stadium
    "VENUEBOS", # TD Garden
    "VENUEBPL", # bp pulse LIVE arena
    "VENUEBREEDERS", # Breeders Cup Mobile
    "VENUEBSA", # Bridgestone Arena
    "VENUEBUFHMK", # Highmark Stadium
    "VENUEBUFKBC", # Key Bank Center
    "VENUECAOMON", # Canadian Open - Montreal
    "VENUECAOTOR", # Canadian Open - Toronto
    "VENUECBS", # Cleveland Browns Stadium
    "VENUECCA", # Crypto.com Arena
    "VENUECFG", # CFG Bank Arena
    "VENUECHA", # Spectrum Center
    "VENUECLBHCS", # Historic Crew Stadium
    "VENUECMN", # CMN Stadium
    "VENUECPA", # Climate Pledge Arena
    "VENUECPKC", # CPKC Stadium
    "VENUECSF", # Charlotte Sports Foundation
    "VENUEDAL", # AT&T Stadium
    "VENUEDTC", # The Delta Center
    "VENUEEDG", # Edgbaston
    "VENUEF1", # Formula 1 - Miami
    "VENUEFLALA", # FLA Live Arena
    "VENUEFRD", # Ford Field
    "VENUEGB", # Lambeau Field
    "VENUEGEO", # GEODIS Park
    "VENUEGIL", # Gillette Stadium
    "VENUEGREYCUP", # Grey Cup
    "VENUEICE", # Ice District
    "VENUEIND", # Bankers Life Fieldhouse
    "VENUELCA", # Little Caesar's Arena
    "VENUELVGPP", # Grand Prix Plaza
    "VENUELVS", # Allegiant Stadium
    "VENUEMC", # Moody Center
    "VENUEMIL", # Fiserv Forum
    "VENUEMIN", # Target Center
    "VENUEMSG", # Madison Square Garden
    "VENUEMSGBCNTHR", # Beacon Theatre
    "VENUEMSGCHITHR", # Chicago Theatre
    "VENUEMSGHLUTHR", # Hulu Theatre
    "VENUEMSGRDOCTY", # Radio City Music Hall
    "VENUENA", # Nationwide Arena
    "VENUENFLMIN", # U.S Bank Stadium
    "VENUENYI", # UBS Arena
    "VENUE02", # O2 Arena
    "VENUEORLKC", # Kia Center
    "VENUEPAT", # Eagle Bank Arena
    "VENUEPC", # Prudential Center
    "VENUEPHX", # Footprint Center
    "VENUEPPG", # PPG Paints Arena
    "VENUERGP", # Rogers Place
    "VENUERQ", # Rose Quarter
    "VENUERSL", # America First Field
    "VENUESAS", # AT&T Center
    "VENUESBA", # Scotiabank Arena
    "VENUESTLCTR", # Enterprise Center
    "VENUESTLTHR", # Stifel Theatre
    "VENUETAS", # MyState Bank Arena
    "VENUETC", # Toyota Center
    "VENUETEN", # Nissan Stadium
    "VENUETMC", # T-Mobile Center
    "VENUETOT", # Tottenham Hotspur Stadium
    "VENUETSA", # Tampa Sports Authority
    "VENUEUAB", # Utilita Arena Birmingham
    "VENUEUBA", # Uber Arena
    "VENUEUBZ", # Uber Platz
    "VENUEUC", # United Center
    "VENUEUEM", # Uber Eats Music Hall
    "VENUEVC", # Verizon Center Mobile
    "VENUEVSH", # Vivint Smart Home Arena
    "VENUEWHA", # Wolverhampton at The Halls
    "VENUEWSH", # Capital One Arena Mobile
    "VENUEXEC", # Xcel Energy Center
    "WNBACHI", # Chicago Sky
    "WNBACON", # Connecticut Sun
    "WNBADAL", # Dallas Wings
    "WNBALVA", # Las Vegas Aces
    "WNBAMIN", # Minnesota Lynx
    "WNBANYL", # New York Liberty
    "WNBAPHO", # Phoenix Mercury Mobile
    "WNBAWAS", # Washington Mystics Mobile
    "XFLLEAGUE", # The Official App of the UFL
    "YCADS", # Test Ads App
    "YCAISLINN", # Aislinn's Demo Corner
    "YCCONCESSIONS", # YinzCam Concessions
    "YCFTP", # YinzCam Free To Play
    "YCPUBLIC", # Public Tenant
    "YCSANDBOX", # YinzCam Sandbox App
    "YCTEST", # YinzCam Test Mobile Apps
    "YCTEST1", # YinzCam FDP Test
]

# 2. Add the Searchable Dropdown
selected_tricode = st.selectbox(
    "Search or Select Application Tricode", 
    options=YINZCAM_TRICODES,
    index=None,
    placeholder="Type to search (e.g., 'PIT' or 'Celtics')...",
    help="Type the tricode or team name to filter the exact app."
)

# 3. The Feature Request Input
user_prompt = st.text_area("Describe the feature or requirement:")

# 4. The Submit Button
if st.button("Draft Sprint Plan", type="primary"):
    
    # 5. The Error Catch
    if not selected_tricode:
        st.error("🚨 Please search and select an Application Tricode first!")
    elif not user_prompt:
        st.error("🚨 Please enter a feature description!")
    else:
        with st.spinner("Analyzing historical Jira data..."):
            
            # Bundle the searched tricode WITH the user's prompt 
            enriched_prompt = f"App Tricode: {selected_tricode}\n\nFeature Request: {user_prompt}"
            
            # Pass the enriched prompt to your agent 
            # sprint_plan_json = agent.generate_plan(enriched_prompt)
            
            # ... rest of your UI code ...
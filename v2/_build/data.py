# Content for the Performadog v2 preview. Facts come from performadog.com.au, the
# Woo catalogue export in rankify-ops/performadog-theme, and Kris's own sites.
# Anything Kris still has to confirm is wrapped in tbc(...) by the templates.

PHONE = "0418 348 804"
FREE_SHIP = 150

# Feeding table printed on the bag (g/day by body weight)
BAG_TABLE = [("5–10 kg", "80–110 g"), ("10–20 kg", "110–140 g"), ("20–30 kg", "140–180 g"),
             ("30–40 kg", "180–220 g"), ("40–50 kg", "220–280 g")]

CURVE = [(2, 45), (7.5, 95), (15, 125), (25, 160), (35, 200), (45, 250), (60, 310)]


def grams(kg):
    for i in range(1, len(CURVE)):
        if kg <= CURVE[i][0]:
            a, b = CURVE[i - 1], CURVE[i]
            t = (kg - a[0]) / (b[0] - a[0])
            return a[1] + t * (b[1] - a[1])
    return CURVE[-1][1]


def per_day(price, bag_kg, dog_kg=30):
    g = round(grams(dog_kg) / 5) * 5
    days = round(bag_kg * 1000 / g)
    return price / days


PRODUCTS = [
    dict(slug="turkey-grain-free", ings=["Turkey","Poultry oil","Lamb","Field peas","Chickpeas","Lentils","Sweet lupins","Egg","Carrots","Spinach","Parsley","Kelp","Tapioca","Yeast extract"], ings_tbc=False, name="Turkey Grain Free", full="Performadog Turkey Grain Free",
         kind="dog", job="Working & sport", code="PD-01", img="performa_GFturkey_lamb-cut.webp",
         sizes=[("2.5 kg", 2.5, 48), ("9 kg", 9, 125), ("15 kg", 15, 168), ("20 kg", 20, None)],
         analysis=[("Crude protein (min)", "32%"), ("Crude fat (min)", "22%"), ("Crude fibre (max)", "4%"),
                   ("Ash (typical)", "7.5%"), ("Calcium", "1.5%"), ("Phosphorus", "1.0%")],
         protein="32", fat="22", ing_key=2,
         blurb="High protein and fat for dogs that train, track, work and compete. Turkey and lamb, no grains, no chicken.",
         long="A concentrated, nutritionally dense diet for canine athletes, dogs with a high workload, and dogs recovering from illness or surgery. The bag puts it plainly: it's built for dogs under high levels of stress — breeding, competition, police and military work.",
         for_who=["Detection, protection and search dogs", "Dog sport and competition", "Breeding dogs", "Recovery after illness or surgery"],
         tags="dog working sport"),
    dict(slug="ocean-fish", ings=["Wild-caught tuna","Lamb","Fish oil","Lamb fat","Rice","Oat groats","Sweet lupins","Alfalfa","Garlic","Carrots","Spinach","Parsley","Kelp","Yeast extract","Methionine"], ings_tbc=True, name="Ocean Fish", full="Performadog Ocean Fish",
         kind="dog", job="Sensitive gut & skin", code="PD-02", img="performa_GF_ocean-fish-cut.webp",
         sizes=[("2.5 kg", 2.5, 48), ("9 kg", 9, 120), ("15 kg", 15, 160), ("20 kg", 20, None)],
         analysis=[("Crude protein (min)", "22%"), ("Crude fat (min)", "14%"), ("Crude fibre (max)", "4%"),
                   ("Ash (typical)", "7%"), ("Calcium", "1.3%"), ("Phosphorus", "0.8%")],
         protein="22", fat="14", ing_key=1,
         blurb="Wild-caught tuna and lamb for dogs with allergies, itchy skin or a touchy stomach. No chicken.",
         long="Wild-caught tuna and lamb with fish oil, kelp and yeast extract. It's the food most owners with itchy, allergic or sensitive dogs end up on — and the one most of the reviews on this site are about.",
         for_who=["Itchy or allergic skin", "Sensitive stomachs and loose stools", "Dogs that can't have chicken", "Everyday adult maintenance"],
         tags="dog sensitive"),
    dict(slug="puppy-lamb-and-fish", ings=["Australian lamb","Wild-caught tuna","Lamb fat","Rice","Oat groats","Sweet lupins","Carrots","Spinach","Parsley","Kelp","Yeast extract","Yucca schidigera"], ings_tbc=True, name="Puppy Lamb & Fish", full="Performadog Puppy Lamb & Fish",
         kind="dog", job="Growth", code="PD-03", img="01_Performadog_Puppy-Single-cut.webp",
         sizes=[("2.5 kg", 2.5, 48), ("9 kg", 9, 125), ("15 kg", 15, 168), ("20 kg", 20, None)],
         analysis=[("Crude protein (min)", "29%"), ("Crude fat (min)", "18%"), ("Crude fibre (max)", "3%"),
                   ("Ash (typical)", "10%"), ("Calcium", "1.9%"), ("Phosphorus", "1.4%")],
         analysis_tbc=True, protein="29", fat="18", ing_key=0,
         blurb="Chicken-free growth food for brain, bone and lean muscle. What Von Forell litters are raised on.",
         long="Australian lamb and wild-caught tuna with rice, oat groats and vegetables. Built as a sole food for growing puppies — brain, bone and lean muscle — and fed to the Von Forell litters from weaning.",
         for_who=["Puppies from weaning", "Large and working breeds while they grow", "Litters (breeders)", "Pups that can't have chicken"],
         tags="dog puppy"),
    dict(slug="purple-boost", name="Purple Boost", full="Purple Boost", kind="supplement", job="Gut support topper",
         code="PB", img="purple_boost_3-cut.webp",
         sizes=[("180 g", 0.18, 43), ("1.08 kg", 1.08, 190)],
         analysis=[("Purple carrot juice powder", "1 kg from 13 kg carrots"), ("Probiotic", "9 strains, 134M CFU/g"),
                   ("Prebiotic", "Mannan-rich yeast fraction"), ("Dose", "1 scoop (3 g) per 20 kg, daily")],
         blurb="A powder topper: purple carrot, a 9-strain probiotic and a prebiotic yeast fraction. Add it to any bowl.",
         long="Purple carrot juice powder, a nine-strain probiotic and a mannan-rich yeast fraction. One 3 g scoop per 20 kg of dog, sprinkled over the food. It's the add-on Kris and Bill put on their own dogs' bowls.",
         for_who=["Any Performadog or iPurr bowl", "Dogs changing food", "Working dogs under load", "Cats too"],
         tags="supplement"),
    dict(slug="ipurr-kangaroo", ings=["Wild kangaroo","Grass-fed lamb","Lamb fat","Rice","Spinach","Kelp","Taurine","Methionine","Yeast extract"], ings_tbc=True, name="iPurr Kangaroo", full="iPurr Kangaroo Cat Food", kind="cat", job="Cats · all ages",
         code="IP-01", img="iPurr_GFOKangaroo-cut.webp", sizes=[("2.5 kg", 2.5, 48)],
         analysis=[("Crude protein (min)", "28%"), ("Crude fat (min)", "16%"), ("Crude fibre (max)", "3%"),
                   ("Ash (typical)", "6%"), ("Calcium", "1.0%"), ("Phosphorus", "0.9%")], analysis_tbc=True,
         ing_key=3, blurb="Wild kangaroo and grass-fed lamb with taurine. No chicken — made for cats that react to poultry.",
         long="Wild kangaroo and grass-fed lamb, with taurine and low magnesium for urinary health. Made for cats of all ages, and for the ones that react to chicken and poultry meal.",
         for_who=["Cats of all ages", "Cats that react to chicken", "Urinary health (low magnesium)"],
         tags="cat"),
    dict(slug="ipurr-ocean-fish", ings=["Wild-caught tuna","Lamb","Tapioca","Lentils","Chickpeas","Field peas","Kelp","Taurine","Methionine"], ings_tbc=True, name="iPurr Grain Free Ocean Fish", full="iPurr Grain Free Ocean Fish", kind="cat",
         job="Cats · sensitive", code="IP-02", img="iPurr_GFOceanFish-cut.webp", sizes=[("2.5 kg", 2.5, 48)],
         analysis=[("Crude protein (min)", "32%"), ("Crude fat (min)", "16%"), ("Crude fibre (max)", "3%"),
                   ("Ash (typical)", "6%"), ("Calcium", "1.9%"), ("Phosphorus", "1.2%")], analysis_tbc=True,
         ing_key=4, blurb="Wild-caught tuna and lamb, grain free, high in omega-3. For cats with sensitive stomachs or skin.",
         long="Wild-caught tuna and lamb, grain free, with taurine. For cats with sensitive stomachs and skin.",
         for_who=["Sensitive stomachs", "Skin and coat", "Grain-free diets"],
         tags="cat"),
]
BY_SLUG = {p["slug"]: p for p in PRODUCTS}

TIMELINE = [
    ("1980", "First Dobermann. Starts training dogs."),
    ("1982", "Starts breeding under the Von Forell name."),
    ("1984", "Sets up a dog security company in Melbourne."),
    ("1993", "Joins the National Dog Trainers Federation. Starts a frozen semen bank."),
    ("2000", "Founds Detector Dogs Australia."),
    ("2003", "Von Forell Vilco wins the National Australian Schutzhund Championship. NDTF life member."),
    ("2015", "Performadog trials begin in the Von Forell kennel."),
    ("2018", "Nutritionist Bill Wiadrowski joins."),
]

# The eight-marker panel the Shopify build already uses (theme repo, evidence-panel)
MARKERS = [("Haemoglobin", "g/L", "Carries oxygen to working muscle."),
           ("Red cell count", "×10¹²/L", "How many oxygen-carrying cells there are."),
           ("Packed cell volume", "%", "Share of blood made up of red cells."),
           ("White cell count", "×10⁹/L", "Overall immune cell count."),
           ("Neutrophils", "×10⁹/L", "First-response immune cells."),
           ("Total protein", "g/L", "A broad read on nutrition and hydration."),
           ("Albumin", "g/L", "The main blood protein; reflects protein status."),
           ("ALT", "U/L", "A liver enzyme.")]

# Real testimonials from performadog.com.au/testimonials — excerpts are verbatim.
# tags: working sport breeder family sensitive puppy cat. rel: material connection to disclose.
T = [
    dict(id="kern", name="Dr Michael Kern", role="Handler · Perth", dog="Caesar · Von Forell Dobermann", tags="sport working",
         q="We have recently accomplished the highest working dog title in a competition and Performadog has been an essential part of our success.",
         rel="Von Forell dog", feat=True),
    dict(id="craig", name="James Craig", role="Director & handler · Tasmania K9 Search and Rescue", dog="Search and rescue dogs", tags="working",
         q="Since switching to Performadog Super Premium Dry Dog food I've found all my dogs have a huge increase in energy and are able to keep their peak condition in periods of intense work.", feat=True),
    dict(id="allgemein", name="Allgemein Rottweilers", role="Breeders · Melbourne", dog="Swift & Rolex · Rottweilers", tags="breeder sport",
         q="Our 2 year old female 'Swift' and 3 year old male 'Rolex' passed their Endurance Test… To quote our vet 'Rolex is as muscled as a Greyhound.'", feat=True),
    dict(id="wilson", name="Derek Wilson", role="Detection dog handler · Melbourne", dog="Koda · Labrador, medical alert", tags="working",
         q="We constantly get remarks on how good Koda looks and the shine of her coat."),
    dict(id="fazzolari", name="Tony Fazzolari", role="CEO · Premier Protection Services", dog="52 kg Rottweiler & 36 kg American Bulldog", tags="working",
         q="Their muscular development is extraordinary as is their stamina… a 20 kg bag lasts almost two months."),
    dict(id="lynn", name="Michelle Lynn", role="Trainer · Yarra Valley", dog="Sport and scent detection dogs", tags="working sport",
         q="Dog's coats are softer, you feed less of it than other dry food products on the market.", rel="Sells Performadog; trains detection dogs for Detector Dogs Australia"),
    dict(id="seraceno", name="Troy Seraceno", role="Core Canine · board & train", dog="5–10 client dogs a week", tags="working",
         q="What a difference in every Dogs performance and functionality!"),
    dict(id="vincent", name="Graeme Vincent", role="Dog sport", dog="3-year-old Malinois", tags="sport",
         q="I am at the end of the 20 Kg bag and I have dog zooming all over the place when I need it."),
    dict(id="doward", name="Cossette Doward", role="Competitor · Sydney", dog="Two competition dogs", tags="sport",
         q="Finally, a complete food that gives my dogs plenty of energy to last the day, and keeps them lean and competition fit."),
    dict(id="marielle", name="Marielle", role="RYPT Personal Training", dog="Working-line German Shepherd & Akita", tags="sport family",
         q="I have certainly noticed her recovery after any exercise become quicker which is amazing."),
    dict(id="young", name="Adrian Young", role="Melbourne", dog="Floyd · Von Forell German Shepherd + 2", tags="sport",
         q="I have found their stamina levels to be up, and general overall activity is higher than normal.", rel="Von Forell dog"),
    dict(id="hampson", name="Lisa Hampson", role="Victoria", dog="Multiple dogs", tags="family sport",
         q="I noticed a considerable change in their coat condition, muscle tone and stamina."),
    dict(id="talty", name="Brett Talty", role="NSW", dog="2 Jack Russells & 2 Maremmas · Ocean Fish", tags="family",
         q="I've done extensive research into a lot of different foods and Performadog comes out on top by a very long way."),
    dict(id="jones-walker", name="Abigail Jones-Walker", role="Owner", dog="Nala · Labrador · Ocean Fish", tags="sensitive family",
         q="She is of a healthy weight, regularly runs 5km-7km with me (she would run further if I let her), has a great digestive system, and her coat is shiny and thick."),
    dict(id="carrington", name="Gerard Carrington", role="NSW", dog="Denzel · Miniature Fox Terrier", tags="sensitive",
         q="I was so relieved and excited when I noticed improvements in Denzel's skin condition in the first two weeks."),
    dict(id="romeo", name="Drew Romeo", role="Perth", dog="Working dog · Ocean Fish", tags="sensitive working",
         q="I have never seen his fur shine like this before and rebounding energy levels to meet his working requirements."),
    dict(id="mulhall", name="Jess Mulhall", role="Melbourne", dog="Puppies and adults", tags="sensitive family",
         q="Her coat gleamed, her stools were consistent and much smaller and her weight rarely fluctuated."),
    dict(id="basil", name="Margaret Basil", role="Melbourne", dog="Rook · rare breed", tags="sensitive",
         q="This was an absolute first he has ever 'gobbled'… and his stools are actually solid."),
    dict(id="eadweards", name="Linda Eadweards", role="Owner", dog="Labrador · Ocean Fish + Purple Boost", tags="family",
         q="Within one week, his coat was such a brilliant shiny black, he had lost some weight."),
    dict(id="liffen", name="Karly Liffen", role="Owner", dog="German Shepherd & Kelpie cross · Turkey Grain Free", tags="family",
         q="I use the grain free turkey and lamb and both my dogs thrive on it."),
    dict(id="leckie", name="Georgia Leckie", role="Owner", dog="German Shepherd · Ocean Fish", tags="family",
         q="So happy with Performadog Ocean Fish. My GSD continues to thrive on this product."),
    dict(id="walker", name="Joanne Walker", role="Shephaven Kennels · New Zealand", dog="Breeding dogs and litters", tags="breeder puppy",
         q="The litters I have raised have done great and have even growth."),
    dict(id="blackburn", name="Sarah Blackburn", role="Sarolta German Shepherds · New Zealand", dog="German Shepherds", tags="breeder puppy",
         q="I have also used Performadog to wean my litter of puppies and it is a easy and simple to use food."),
    dict(id="jarvis", name="Lavina Jarvis", role="Von Hefner German Shepherd Kennels · Dunedin NZ", dog="German Shepherds", tags="breeder",
         q="The constant shedding of coats experienced has ceased and now we have gleaming, shiny coats and no dryness."),
    dict(id="stice", name="Kath Stice", role="LaRycia Kennels · Dunedin NZ", dog="German Shepherds", tags="breeder puppy",
         q="I started using Performadog and raised my first litter on it at the beginning of 2014. I have not looked back."),
    dict(id="wright", name="Lisa Wright", role="Melbourne", dog="Lulu · Dobermann puppy", tags="puppy",
         q="I have fed my Doberman, Lulu, solely on 'Performadog dry dog food' since the age of 7 weeks."),
    dict(id="devissar", name="Steve De Vissar", role="Melbourne", dog="Hugo · Von Forell German Shepherd", tags="family",
         q="His coat and general condition have never been better, his stools are very consistent, energy levels are through the roof.", rel="Von Forell dog"),
    dict(id="buckland", name="Michael Buckland", role="Queensland", dog="5-year-old German Shepherd", tags="family",
         q="Shipping to Brisbane was fast, (3 days from order to my door) and well-priced."),
    dict(id="wills", name="Karis Wills", role="Perth", dog="German Shepherd", tags="family",
         q="Super Premium Dry Dog Food without the Premium prices."),
    dict(id="thompson", name="Emma Thompson", role="Perth", dog="One large and one small dog", tags="family sensitive",
         q="The smaller biscuit design is great for both our large and small dog."),
    dict(id="mahoney", name="Keryn Mahoney", role="Tasmania", dog="Dobermanns & Dachshunds", tags="family sport",
         q="On a recent visit to the vet… he noted how good the four dogs teeth were, to quote him 'Whatever you are feeding them, keep feeding it'.",
         rel="Tasmanian distributor"),
    dict(id="kawecki", name="Sue Kawecki", role="Obedience & tracking competitor · Melbourne", dog="German Shepherd", tags="sport",
         q="My dog has been fed the food from a puppy to her adult life… her coat has always looked shiny and healthy."),
    dict(id="scott", name="Vaughan Scott", role="Western Australia", dog="Von Forell German Shepherd", tags="family",
         q="My dog has loads of energy and is always in excellent physical condition.", rel="Von Forell dog"),
    dict(id="mariettakis", name="Victoria Mariettakis", role="Owner", dog="Devon Rex · iPurr Kangaroo", tags="cat",
         q="My girl is now back at a healthy weight and her fur although already silky soft is even softer."),
]

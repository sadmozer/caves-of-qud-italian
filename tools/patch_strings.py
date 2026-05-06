#!/usr/bin/env python3
"""
Inserts all missing entries from Strings.example.xml into Strings.it.xml,
with Italian translations where available.
"""
import xml.etree.ElementTree as ET
import re, html, sys

SRC = '/mnt/c/Users/ncard/Desktop/GameDev/caves-of-qud-italian/ExampleLanguage/Strings.example.xml'
IT  = '/mnt/c/Users/ncard/Desktop/GameDev/caves-of-qud-italian/ItalianLanguage/languages/Strings.it.xml'

# ── Translation dictionary ─────────────────────────────────────────────────
TRANS = {

# ── Tutorial BattleRemains ─────────────────────────────────────────────────
"Let's take another look at weapon stats. Next to the {{c|→}} is 5. That means you'll usually penetrate the armor of a creature with AV equal to 5.\n\nYou can penetrate armor multiple times, though, and each time you penetrate, you deal the weapon's damage.\n\nLet's equip it.":
"Ancora sulle statistiche delle armi. Accanto a {{c|→}} c'è 5: di solito penetrerai l'armatura di creature con AV pari a 5.\n\nÈ possibile penetrare più volte: ogni penetrazione infligge i danni dell'arma.\n\nEquipaggila.",

"A battle axe. Get it.\n\nHit =commandKey:CmdUse=":
"Un'ascia da guerra. Raccoglila.\n\nPremi =commandKey:CmdUse=",

"A battle axe. Get it.\n\nHit =commandKey:CmdGet=":
"Un'ascia da guerra. Raccoglila.\n\nPremi =commandKey:CmdGet=",

"Let's take a look at the Equipment screen.\n\nPress =commandKey:CmdCharacter=":
"Apriamo la schermata Equipaggiamento.\n\nPremi =commandKey:CmdCharacter=",

"Let's take a look at the Equipment screen.\n\nPress =commandKey:CmdEquipment=":
"Apriamo la schermata Equipaggiamento.\n\nPremi =commandKey:CmdEquipment=",

"Select the Inventory && Equipment tab.\n\nYou can use =commandKey:Page Left= and =commandKey:Page Right= to navigate between tabs.":
"Seleziona la scheda Inventario && Equipaggiamento.\n\nUsa =commandKey:Page Left= e =commandKey:Page Right= per navigare tra le schede.",

# ── Tutorial ExamineChemcell ───────────────────────────────────────────────
"The bear is dead! Looks like it dropped something, too.\n\nBut first, let's use this opportunity to heal.":
"L'orso è morto! Ha lasciato cadere qualcosa.\n\nPrima però, sfruttiamo l'occasione per curarci.",

"You regain hitpoints naturally as turns pass. You can pass a few turns by waiting, or if there are no hostile creatures around, you can {{W|rest until healed}}.\n\nPress =commandKey:CmdWaitUntilHealed=":
"Punti vita si recuperano naturalmente. Puoi attendere qualche turno, oppure, se non ci sono creature ostili, {{W|riposare fino a guarigione}}.\n\nPremi =commandKey:CmdWaitUntilHealed=",

"You picked up the odd trinket automatically because it is an artifact.\n\nPress =commandKey:CmdCharacter= to investigate it.":
"Hai raccolto il curioso oggetto automaticamente perché è un artefatto.\n\nPremi =commandKey:CmdCharacter= per esaminarlo.",

"You picked up the odd trinket automatically because it is an artifact.\n\nPress =commandKey:CmdInventory= to investigate it.":
"Hai raccolto il curioso oggetto automaticamente perché è un artefatto.\n\nPremi =commandKey:CmdInventory= per esaminarlo.",

# ── Tutorial ExploreJoppa ──────────────────────────────────────────────────
"Oh! it looks like Warden Yrame killed Mehmet. Why, you ask?\n\nWell, named creatures who you can perform the water ritual with, like Mehmet, generate with dynamic faction relationships. In your game, Mehmet must have been hated by the Fellowship of Wardens for some reason.":
"Oh! Sembra che Warden Yrame abbia ucciso Mehmet. Come mai?\n\nLe creature nominate come Mehmet generano relazioni frazionali dinamiche. In questa partita, Mehmet era odiato dalla Compagnia delle Guardie.",

"And so Warden Yrame took her revenge. In Qud, sometimes even our best efforts at providing a safe starter village are foiled by the simulation!\n\nWhat a charmed run! It's quite rare for this to happen, but now you get to see this hidden section of the tutorial. Good job.":
"E così Warden Yrame si è vendicata. A Qud, anche i nostri sforzi per garantire un villaggio iniziale sicuro vengono a volte vanificati dalla simulazione!\n\nChe avventura! È piuttosto raro, ma ora puoi vedere questa sezione nascosta del tutorial. Ottimo lavoro.",

"You have a few options now. You can roll with it and continue in this world where Mehmet's been revenge-slain. The early game will be a bit harder, but the main quest is not impacted.\n\nYou can start over and play the tutorial again, for the \"normal\" ending, which you were about to reach.\n\nOr, since you were near the end anyway, you can start a new game and begin your journey proper!":
"Ora hai diverse opzioni. Puoi continuare in questo mondo dove Mehmet è stato ucciso. L'inizio sarà più difficile, ma la quest principale non ne risente.\n\nPuoi ricominciare il tutorial per il finale \"normale\".\n\nOppure, visto che eri quasi alla fine, inizia una nuova partita e comincia il vero viaggio!",

"Whatever you choose, good luck, and feel free to return here for a refresher.\n\nLive and drink.":
"Qualunque cosa tu scelga, buona fortuna. Torna qui quando vuoi rinfrescarti la memoria.\n\nVivi e bevi.",

"Quetzal! That's all for the tutorial, friend.\n\nWe just scratched the very tip of the surface. Quests, secrets, leveling up, physics, reputation, limbs... we leave that for you to discover.":
"Quetzal! Il tutorial è terminato, amico.\n\nAbbiamo appena scalfito la superficie. Quest, segreti, livellamento, fisica, reputazione, arti... lasciamo a te il piacere di scoprirli.",

"You can see a list of points of interest by pressing =commandKey:CmdMoveToPointOfInterest=.\n\nThe list will grow as you explore more of the map.":
"Puoi vedere l'elenco dei punti di interesse premendo =commandKey:CmdMoveToPointOfInterest=.\n\nL'elenco cresce man mano che esplori la mappa.",

"You can see a list of points of interest by clicking this button or pressing =commandKey:CmdMoveToPointOfInterest=.\n\nThe list will grow as you explore more of the map.":
"Puoi vedere l'elenco dei punti di interesse cliccando questo pulsante o premendo =commandKey:CmdMoveToPointOfInterest=.\n\nL'elenco cresce man mano che esplori la mappa.",

# ── Tutorial ExploreStairs ─────────────────────────────────────────────────
"Ascend.\n\nPress =commandKey:CmdMoveU=.":
"Ascendi.\n\nPremi =commandKey:CmdMoveU=.",

"Ascend.\n\nYou can click this button or press =commandKey:CmdMoveU=.":
"Ascendi.\n\nPuoi cliccare questo pulsante o premere =commandKey:CmdMoveU=.",

# ── Tutorial ExploreWorldMap ───────────────────────────────────────────────
"You'll be able to explore the world freely after the tutorial.\n\nFor now, let's visit Joppa.":
"Potrai esplorare il mondo liberamente dopo il tutorial.\n\nPer ora, visitiamo Joppa.",

"You can look around here just like on a local map.\n\nUse =commandKey:LookDirection=":
"Puoi guardarti intorno come su una mappa locale.\n\nUsa =commandKey:LookDirection=",

"You can look around here just like on a local map.\n\nPress =commandKey:CmdLook=":
"Puoi guardarti intorno come su una mappa locale.\n\nPremi =commandKey:CmdLook=",

"Descend.\n\nPress =commandKey:CmdMoveD=.":
"Discendi.\n\nPremi =commandKey:CmdMoveD=.",

"Descend.\n\nYou can click this button or press =commandKey:CmdMoveD=.":
"Discendi.\n\nPuoi cliccare questo pulsante o premere =commandKey:CmdMoveD=.",

"There's a village to the north called Joppa. Let's go there.\n\nHold =commandKey:IndicateDirection= towards the north and press =commandKey:Take A Step=.":
"A nord c'è un villaggio chiamato Joppa. Andiamoci.\n\nTieni premuto =commandKey:IndicateDirection= verso nord e premi =commandKey:Take A Step=.",

"There's a village to the north called Joppa. Let's go there.\n\nPress =commandKey:CmdMoveN= or =commandKey:AdventureMouseContextAction=.":
"A nord c'è un villaggio chiamato Joppa. Andiamoci.\n\nPremi =commandKey:CmdMoveN= o =commandKey:AdventureMouseContextAction=.",

# ── Tutorial FightBear ─────────────────────────────────────────────────────
"Oh! Another creature. Let's look at it more closely.\n\nWhen you come across something new, it's always a good idea to inspect it.":
"Oh! Un'altra creatura. Osserviamola da vicino.\n\nQuando incontri qualcosa di nuovo, è sempre una buona idea esaminarlo.",

"Look view lets you look around and investigate your surroundings.\n\nMove the cursor to the bear.":
"La modalità Osserva permette di guardarsi intorno e investigare l'ambiente.\n\nSposta il cursore sull'orso.",

"You can wait a turn for the bear to approach. That way, it won't be in range to attack you when it takes its turn.\n\nTap =commandKey:Take A Step= without choosing a direction with the stick to pass a turn.":
"Puoi aspettare un turno affinché l'orso si avvicini. Così non sarà a portata di attacco quando tocca a lui.\n\nPremi =commandKey:Take A Step= senza scegliere una direzione per passare un turno.",

"You can wait a turn for the bear to approach. That way, it won't be in range to attack you when it takes its turn.\n\nPress =commandKey:CmdWait:allbinds= or =commandKey:AdventureMouseContextAction= on your character to pass a turn.":
"Puoi aspettare un turno affinché l'orso si avvicini. Così non sarà a portata di attacco quando tocca a lui.\n\nPremi =commandKey:CmdWait:allbinds= o =commandKey:AdventureMouseContextAction= sul personaggio per passare un turno.",

"You missed, then the bear attacked and missed.\n\nAttack again.":
"Hai mancato, poi l'orso ha attaccato e mancato.\n\nAttacca di nuovo.",

"This time you hit, but you failed to penetrate the bear's armor.\n\nThen, the bear hit you and DID penetrate your armor. You took 4 damage.":
"Stavolta hai colpito, ma non hai penetrato l'armatura dell'orso.\n\nPoi l'orso ti ha colpito e HA penetrato la tua armatura. Hai subito 4 danni.",

"Let's try using an ability. Look at your ability bar. Let's start sprinting. \n\nSelect it with =commandKey:Next Ability= and =commandKey:Previous Ability= then press =commandKey:Use Ability=.":
"Proviamo a usare un'abilità. Guarda la barra delle abilità. Iniziamo a scattare.\n\nSelezionala con =commandKey:Next Ability= e =commandKey:Previous Ability=, poi premi =commandKey:Use Ability=.",

"Every character has Sprint, but most of your abilities are determined by traits like your mutations. You have Freezing Ray, so you can shoot frost out of your hands.\n\nSelect it with =commandKey:Next Ability= and =commandKey:Previous Ability= then press =commandKey:Use Ability=.":
"Ogni personaggio ha Scatto, ma molte abilità derivano da tratti come le mutazioni. Hai Raggio Congelante: spari gelo dalle mani.\n\nSelezionala con =commandKey:Next Ability= e =commandKey:Previous Ability=, poi premi =commandKey:Use Ability=.",

"Every character has Sprint, but most of your abilities are determined by traits like your mutations. You have Freezing Ray, so you can shoot frost out of your hands. Select it.\n\nPress =commandKey:CmdAbility2=":
"Ogni personaggio ha Scatto, ma molte abilità derivano da tratti come le mutazioni. Hai Raggio Congelante: spari gelo dalle mani. Selezionala.\n\nPremi =commandKey:CmdAbility2=",

# ── Tutorial FightSnapjaw ──────────────────────────────────────────────────
"Let's explore further into the cave.\n\nWalk down the passage.":
"Esploriamo più a fondo nella caverna.\n\nCammina lungo il passaggio.",

"Look view lets you look around and investigate your surroundings.\n\nMove the cursor to the snapjaw.":
"La modalità Osserva permette di guardarsi intorno e investigare l'ambiente.\n\nSposta il cursore sullo snapjaw.",

"All actions are turn-based, meaning you take a turn, then other creatures take a turn. For the most part, creatures won't act until you do.\n\nIf you ever get panicked, just slow down and consider your next move. There's no rush.":
"Tutte le azioni sono a turni: prima agisci tu, poi le altre creature. In genere le creature non agiscono finché non lo fai tu.\n\nSe ti prende il panico, rallenta e considera la prossima mossa. Non c'è fretta.",

"You can pick up things that are in the same space as you.\n\nPress =commandKey:CmdUse=":
"Puoi raccogliere oggetti nello stesso spazio.\n\nPremi =commandKey:CmdUse=",

"You can pick up things that are in the same space as you.\n\nPress =commandKey:CmdGet=":
"Puoi raccogliere oggetti nello stesso spazio.\n\nPremi =commandKey:CmdGet=",

"Whew! You killed the snapjaw and earned some experience. It looks like they dropped a piece of equipment, too.\n\nPress =commandKey:CmdGetFrom= and then choose a direction.":
"Ottimo! Hai ucciso lo snapjaw e guadagnato esperienza. Ha lasciato cadere un equipaggiamento.\n\nPremi =commandKey:CmdGetFrom= e scegli una direzione.",

"Whew! You killed the snapjaw and earned some experience. It looks like they dropped a piece of equipment, too.\n\nPress =commandKey:CmdGetFrom= and then choose a direction or press =commandKey:AdventureMouseInteract=.":
"Ottimo! Hai ucciso lo snapjaw e guadagnato esperienza. Ha lasciato cadere un equipaggiamento.\n\nPremi =commandKey:CmdGetFrom= e scegli una direzione o premi =commandKey:AdventureMouseInteract=.",

"Let's look at the leather armor you picked up.\n\nArmor has an armor value (=av:2=) and a dodge value (=dv:0=)\n\nBoth help you avoid damage.":
"Esaminiamo l'armatura di cuoio raccolta.\n\nArmatura ha un valore armatura (=av:2=) e un valore schivata (=dv:0=).\n\nEntrambi aiutano a evitare danni.",

"You can also equip items by dragging them from your inventory to their equipment slot.\n\nBy the way, you have several other tabs in your character sheet. Feel free to explore them later.":
"Puoi anche equipaggiare oggetti trascinandoli dall'inventario allo slot di equipaggiamento.\n\nHai altre schede nella scheda personaggio. Esplorali quando vuoi.",

# ── Tutorial GetBooks ──────────────────────────────────────────────────────
"Sometimes squares have multiple items in them.\n\nTo see everything in a space, press =commandKey:CmdGetFrom= and then choose a direction.":
"A volte uno spazio contiene più oggetti.\n\nPer vedere tutto, premi =commandKey:CmdGetFrom= e scegli una direzione.",

"Sometimes squares have multiple items in them.\n\nTo see everything in a space, press =commandKey:CmdGetFrom= and then choose a direction or press =commandKey:AdventureMouseInteractAll=.":
"A volte uno spazio contiene più oggetti.\n\nPer vedere tutto, premi =commandKey:CmdGetFrom= e scegli una direzione o premi =commandKey:AdventureMouseInteractAll=.",

"Whoever this was, they had some books. All books can be read in game.\n\nBooks with {{Y|white}} titles are generated and usually contain nonsense, but the nonsense can occasionally be useful.\n\nBooks with {{W|gold}} titles are more valuable: they are handwritten by in-world beings and contain interesting takes on the world.":
"Chiunque fosse, aveva dei libri. Tutti i libri possono essere letti in gioco.\n\nI libri con titoli {{Y|bianchi}} sono generati e contengono di solito sciocchezze, ma a volte utili.\n\nI libri con titoli {{W|dorati}} sono più preziosi: scritti a mano da esseri del mondo e ricchi di visioni interessanti.",

# ── IntroTutorial ──────────────────────────────────────────────────────────
"Welcome to the Caves of Qud tutorial. We'll just be scratching the surface here, learning enough of the basics to help you get your footing.\n\nIn Caves of Qud, you play as a mutated human or true kin.\n\nFor the tutorial, we're picking mutated human.":
"Benvenuto nel tutorial di Caves of Qud. Scalfiremo appena la superficie, imparando le basi per muovere i primi passi.\n\nIn Caves of Qud si gioca come umano mutato o puro.\n\nPer il tutorial, scegliamo umano mutato.",

"Character creation is a deep and sometimes long process. We included some preset builds to help you get started. After the tutorial, you can try another build, or make a character from scratch. (The recommended way! Once you get your footing.) \n\nFor now, pick the marsh taur.":
"La creazione del personaggio è un processo profondo e a volte lungo. Abbiamo incluso alcune build preimpostate per aiutarti. Dopo il tutorial, puoi provare un'altra build o creare un personaggio da zero. (Il modo consigliato, una volta acquisita familiarità.)\n\nPer ora, scegli il marsh taur.",

# ── Tutorial MakeCamp ──────────────────────────────────────────────────────
"Let's not be rude. Talk to the beetle.\n\nPress =commandKey:CmdUse=.":
"Non essere scortese. Parla con lo scarabeo.\n\nPremi =commandKey:CmdUse=.",

"Let's not be rude. Talk to the beetle.\n\nPress =commandKey:CmdUse= or =commandKey:AdventureMouseContextAction=.":
"Non essere scortese. Parla con lo scarabeo.\n\nPremi =commandKey:CmdUse= o =commandKey:AdventureMouseContextAction=.",

"Not much of a talker. But that's not true for everyone. As long as a creature isn't hostile, you can try to chat with them.\n\nLet's see what the beetle has for trade.":
"Non molto loquace. Ma non è così per tutti. Finché una creatura non è ostile, puoi parlarle.\n\nVediamo cosa ha lo scarabeo da scambiare.",

"The beetle's inventory is on the left, and your inventory is on the right.\n\nThe beetle has some witchwood bark. That's useful — it heals you when you eat it. Let's trade for it.":
"L'inventario dello scarabeo è a sinistra, il tuo a destra.\n\nLo scarabeo ha della corteccia di witchwood. Utile: guarisce quando mangiata. Facciamo uno scambio.",

"The beetle has some witchwood bark. That's useful — it heals you when you eat it. Let's trade for it.\n\nPress =commandKey:CmdTradeAdd=":
"Lo scarabeo ha della corteccia di witchwood. Utile: guarisce quando mangiata.\n\nPremi =commandKey:CmdTradeAdd=",

"The beetle has some witchwood bark. That's useful — it heals you when you eat it. Let's trade for it.\n\nPress =commandKey:CmdTradeAdd= or =commandKey:AdventureMouseContextAction=":
"Lo scarabeo ha della corteccia di witchwood. Utile: guarisce quando mangiata.\n\nPremi =commandKey:CmdTradeAdd= o =commandKey:AdventureMouseContextAction=",

"We don't need this dagger any more, so we can trade it away.\n\nPress =commandKey:CmdTradeAdd=":
"Non abbiamo più bisogno di questo pugnale, possiamo scambiarlo.\n\nPremi =commandKey:CmdTradeAdd=",

"We don't need this dagger any more, so we can trade it away.\n\nPress =commandKey:CmdTradeAdd= or =commandKey:AdventureMouseContextAction=":
"Non abbiamo più bisogno di questo pugnale, possiamo scambiarlo.\n\nPremi =commandKey:CmdTradeAdd= o =commandKey:AdventureMouseContextAction=",

"The trade is uneven, so we'll have to pony up some money.\n\nIn the salt-stippled ecosystem of Qud, {{B|fresh water}} is currency. You need to drink it, too, so don't spend it all.":
"Lo scambio è sbilanciato, dobbiamo aggiungere denaro.\n\nNell'ecosistema salato di Qud, {{B|acqua fresca}} è la valuta. Si usa anche per bere, quindi non spenderla tutta.",

"Now to go to the world map. Try ascending again.\n\nPress =commandKey:CmdMoveU=.":
"Ora andiamo alla mappa del mondo. Prova ad ascendere di nuovo.\n\nPremi =commandKey:CmdMoveU=.",

"Now to go to the world map. Try ascending again.\n\nYou can click this button or press =commandKey:CmdMoveU=.":
"Ora andiamo alla mappa del mondo. Prova ad ascendere di nuovo.\n\nPuoi cliccare questo pulsante o premere =commandKey:CmdMoveU=.",

# ── Tutorial MoveToChest ───────────────────────────────────────────────────
"This is the main gameplay stage. At the top of the screen are your attributes, HP, and XP.\n\nOn the right are action buttons, minimap, and the message log.\n\nAt the bottom is your ability hotbar.":
"Questa è la schermata principale di gioco. In alto: attributi, VP e XP.\n\nA destra: pulsanti azione, minimappa e registro messaggi.\n\nIn basso: la barra rapida delle abilità.",

"Huh, you destroyed the tutorial chest we were going to teach you how to use.\n\nGo ahead and pick of the torch and dagger from the floor.":
"Ehm, hai distrutto il baule del tutorial. Raccogli pure la torcia e il pugnale dal pavimento.",

"You can interact with objects you're next to. Open the chest.\n\nPress =commandKey:Accept=":
"Puoi interagire con gli oggetti vicini. Apri il baule.\n\nPremi =commandKey:Accept=",

"You can interact with objects you're next to. Open the chest.\n\nPress =commandKey:Accept= or =commandKey:AdventureMouseContextAction=":
"Puoi interagire con gli oggetti vicini. Apri il baule.\n\nPremi =commandKey:Accept= o =commandKey:AdventureMouseContextAction=",

"Looks like there's a chest over at the end of the room. Let's walk over to it.\n\nHold =commandKey:IndicateDirection= in the direction you want to move and press =commandKey:Take A Step=.":
"Sembra esserci un baule in fondo alla stanza. Andiamoci.\n\nTieni premuto =commandKey:IndicateDirection= nella direzione desiderata e premi =commandKey:Take A Step=.",

"Looks like there's a chest over at the end of the room. Let's walk over to it.\n\nYou can click =commandKey:AdventureNavMouseLeftClick= the square you want to move to, or use the {{hotkey|arrow keys}} or {{hotkey|numpad.}}\n\nWith arrow keys, you can press {{hotkey|shift+arrow keys}} to move diagonally.":
"Sembra esserci un baule in fondo alla stanza. Andiamoci.\n\nPuoi cliccare =commandKey:AdventureNavMouseLeftClick= sul quadrato verso cui muoverti, o usare {{hotkey|frecce}} o {{hotkey|tastierino numerico.}}\n\nCon le frecce, premi {{hotkey|shift+frecce}} per muoverti in diagonale.",

# ── Tutorial Death ─────────────────────────────────────────────────────────
"Oh, you died. That's okay. It's a very common occurance in the world of Qud.\n\nBecause the tutorial drops you off in Classic mode with permadeath, your character is wiped when you die.\n\nThe good news is: you get to make a whole new character! Now with a little more knowledge than you had before.":
"Sei morto. Va bene. È un evento molto comune nel mondo di Qud.\n\nPoiché il tutorial usa la modalità Classica con morte permanente, il personaggio viene cancellato alla morte.\n\nLa buona notizia: puoi creare un personaggio completamente nuovo, con un po' più di esperienza.",

"Next time, if you want a more forgiving mode of play, try Roleplay, which lets you checkpoint at settlements.\n\nOr try Wander mode, where most creatures are neutral to you and you gain experience via discovery instead of killing.\n\nOr keep playing Classic if the challenge appeals to you and you'd like to explore a breadth of character types.":
"La prossima volta, per una modalità più clemente, prova Roleplay: permette checkpoint negli insediamenti.\n\nO prova la modalità Vagabondo, dove molte creature sono neutrali e si guadagna esperienza tramite scoperte invece che uccisioni.\n\nOppure continua con Classica se la sfida ti attrae e vuoi esplorare vari tipi di personaggio.",

"Whatever you choose next, feel free to return to the tutorial if you need a refresher.\n\nLive and drink, friend!":
"Qualunque cosa tu scelga, torna al tutorial quando vuoi rinfrescarti la memoria.\n\nVivi e bevi, amico!",

# ── GameSummary Ultimate endings ───────────────────────────────────────────
"You annulled the plagues of the Gyre.\n\nThen you freed the Spindle for another's ascent and crossed into Brightsheol":
"Hai annullato le piaghe del Gyre.\n\nHai liberato lo Spindle per l'ascesa altrui e attraversato verso Brightsheol.",

"You annulled the plagues of the Gyre.\n\nThen you destroyed Resheph to save the burgeoning world but marooned yourself at the North Sheva.":
"Hai annullato le piaghe del Gyre.\n\nHai distrutto Resheph per salvare il mondo in fioritura, ma sei rimasto abbandonato al North Sheva.",

"You annulled the plagues of the Gyre.\n\nThen you entered into a covenant with Resheph to help prepare Qud for the Coven's return.":
"Hai annullato le piaghe del Gyre.\n\nHai stretto un patto con Resheph per preparare Qud al ritorno del Coven.",

"You annulled the plagues of the Gyre.\n\nThen you destroyed Resheph and returned to Qud to help garden the burgeoning world.":
"Hai annullato le piaghe del Gyre.\n\nHai distrutto Resheph e sei tornato a Qud per coltivare il mondo in fioritura.",

"You annulled the plagues of the Gyre.\n\nThen you returned to Qud to help garden the burgeoning world.":
"Hai annullato le piaghe del Gyre.\n\nSei tornato a Qud per coltivare il mondo in fioritura.",

"You annulled the plagues of the Gyre.\n\nThen you reversed course and acceded to Resheph's plan to purge the world of higher life, in preparation for the Coven's return.":
"Hai annullato le piaghe del Gyre.\n\nHai invertito rotta e acconsentito al piano di Resheph di purgare il mondo dalla vita superiore, in preparazione al ritorno del Coven.",

"You annulled the plagues of the Gyre.\n\nThen you destroyed Resheph and launched yourself into the dusted cosmos to ply the stars with Barathrum.":
"Hai annullato le piaghe del Gyre.\n\nHai distrutto Resheph e ti sei lanciato nel cosmo polveroso per solcare le stelle con Barathrum.",

"You annulled the plagues of the Gyre.\n\nThen you destroyed Resheph and launched yourself into the dusted cosmos to ply the stars.":
"Hai annullato le piaghe del Gyre.\n\nHai distrutto Resheph e ti sei lanciato nel cosmo polveroso per solcare le stelle.",

"You annulled the plagues of the Gyre.\n\nThen you launched yourself into the dusted cosmos to ply the stars with Barathrum.":
"Hai annullato le piaghe del Gyre.\n\nTi sei lanciato nel cosmo polveroso per solcare le stelle con Barathrum.",

"You annulled the plagues of the Gyre.\n\nThen you launched yourself into the dusted cosmos to ply the stars.":
"Hai annullato le piaghe del Gyre.\n\nTi sei lanciato nel cosmo polveroso per solcare le stelle.",

# ── UI / Popups ────────────────────────────────────────────────────────────
"Your tombstone file was saved:\n\n=filename=":
"Il file della lapide è stato salvato:\n\n=filename=",

"Note: Playing a saved game in a language other than that game's original language will result in partial and incomplete translations.\n\nChanging language requires restart.":
"Nota: caricare un salvataggio in una lingua diversa dall'originale produrrà traduzioni parziali e incomplete.\n\nCambiare lingua richiede riavvio.",

"That save file looks like it's from an older save format revision (=gameVersion=). Sorry!\n\nYou can probably change to a previous branch in your game client and get it to load if you want to finish it off.":
"Salvataggio di revisione precedente (=gameVersion=). Spiacenti!\n\nPotresti passare a un ramo precedente del client per aprirlo.",

"ABILITIES\npage =current= of =total=":
"ABILITÀ\npagina =current= di =total=",

"Hot Loading Books...\n":
"Caricamento rapido libri...\n",

"If you quit without saving, you will lose all your progress and your character will be lost. Are you sure you want to QUIT and LOSE YOUR PROGRESS?\n\nType '=abandonConfirm=' to confirm.":
"Uscendo senza salvare perderai tutti i progressi e il personaggio andrà perduto. Sei sicuro di voler USCIRE e PERDERE I PROGRESSI?\n\nDigita '=abandonConfirm=' per confermare.",

"If you quit without saving, you will lose all your unsaved progress. Are you sure you want to QUIT and LOSE YOUR PROGRESS?\n\nType '=abandonConfirm=' to confirm.":
"Uscendo senza salvare perderai i progressi non salvati. Sei sicuro di voler USCIRE e PERDERE I PROGRESSI?\n\nDigita '=abandonConfirm=' per confermare.",

"If you quit without saving, you will lose all your unsaved progress. Are you sure you want to QUIT and LOSE YOUR PROGRESS?\n\nType 'ABANDON' to confirm.":
"Uscendo senza salvare perderai i progressi non salvati. Sei sicuro di voler USCIRE e PERDERE I PROGRESSI?\n\nDigita 'ABANDON' per confermare.",

"=warnings=\n\nContinue anyway?":
"=warnings=\n\nContinuare comunque?",

# ── Core game summary / end ────────────────────────────────────────────────
"{{C|=ind=}} Game summary for {{W|=player.name=}} {{C|=ind=}}\n\n":
"{{C|=ind=}} Sommario partita per {{W|=player.name=}} {{C|=ind=}}\n\n",

"This game ended on =longDate= at =longTime=.\n":
"Partita terminata: =longDate= alle =longTime=.\n",

"You were level {{C|=level=}}.\nYou scored {{C|=score=}} =score.pluralize:point=.\n":
"Livello raggiunto: {{C|=level=}}.\nPunteggio: {{C|=score=}}.\n",

"You survived for {{C|=turns=}} =turns.pluralize:turn=.\n":
"Turni sopravvissuti: {{C|=turns=}}.\n",

"You found {{C|=lairs=}} =lairs.pluralize:lair=.\n":
"Rifugi scoperti: {{C|=lairs=}}.\n",

"You found {{C|=items=}} =items.pluralize:item=.\n":
"Oggetti trovati: {{C|=items=}}.\n",

"You generated {{C|=artifacts=}} storied =artifacts.pluralize:item=.\n":
"Artefatti con storia: {{C|=artifacts=}}.\n",

"The most advanced artifact in your possession was =artifact.a.name:asIfKnown:noConfusion=.\n":
"Artefatto più avanzato: =artifact.a.name:asIfKnown:noConfusion=.\n",

"This game was played in =game.mode= mode.\n":
"Modalità di gioco: =game.mode=.\n",

"\n\n{{C|=ind=}} Chronology for {{W|=player.name=}} {{C|=ind=}}\n\n":
"\n\n{{C|=ind=}} Cronologia per {{W|=player.name=}} {{C|=ind=}}\n\n",

"\n\n{{C|=ind=}} Final Messages for {{W|=player.name=}} {{C|=ind=}}\n\n":
"\n\n{{C|=ind=}} Messaggi Finali per {{W|=player.name=}} {{C|=ind=}}\n\n",

# ── Chargen ────────────────────────────────────────────────────────────────
"{{C|-2 License Tier\n+1 Toughness}}":
"{{C|-2 Livello Licenza\n+1 Robustezza}}",

# ── Quest dialogs ──────────────────────────────────────────────────────────
"Are you seeking more work, =player.formalAddressTerm=? Recently we came into possession of a data disk bearing a peculiar stamp and encoded with a strange signal. The signal means nothing to us, but there's a sect of tinkers called the Barathrumites who might be interested in it. They are friends to our village and often trade for the scrap we tow out of the earth. Would you carry the disk to their enclave at Grit Gate, along the western rim of the jungle? In exchange for the delivery, you might seek an apprenticeship with them.\n\nIf you are interested, take the disk now, and travel safely.":
"Cerchi altro lavoro, =player.formalAddressTerm=? Di recente siamo entrati in possesso di un disco dati con uno strano sigillo, codificato con un segnale misterioso. Il segnale non ci dice nulla, ma c'è una setta di artigiani chiamata i Barathrumiti che potrebbe trovarlo interessante. Amici del villaggio, commerciano i rottami che estraiamo dalla terra. Porteresti il disco alla loro enclave a Grit Gate, lungo il margine occidentale della giungla? In cambio della consegna, potresti cercare un apprendistato con loro.\n\nSe sei interessato, prendi il disco ora e viaggia in sicurezza.",

"=spice:quests.FindaSite.travelers.intro.!random|capitalize= =spice:quests.FindaSite.travelers.cameToOurVillage.!random|capitalize=. =spice:quests.FindaSite.travelers.spokeOfPlace.!random|capitalize|a.to.an=. But they wouldn't reveal the location. =spice:quests.FindaSite.travelers.wouldYouFindIt.!random|capitalize= =spice:quests.FindaSite.travelers.greatBoon.!random|capitalize=. =spice:quests.FindaSite.travelers.rewardYou.!random|capitalize=.\n\n=spice:quests.FindaSite.typeOfDirections.$typeOfDirections.intro.!random|capitalize=.":
"=spice:quests.FindaSite.travelers.intro.!random|capitalize= =spice:quests.FindaSite.travelers.cameToOurVillage.!random|capitalize=. =spice:quests.FindaSite.travelers.spokeOfPlace.!random|capitalize|a.to.an=. Ma non vollero rivelare il luogo. =spice:quests.FindaSite.travelers.wouldYouFindIt.!random|capitalize= =spice:quests.FindaSite.travelers.greatBoon.!random|capitalize=. =spice:quests.FindaSite.travelers.rewardYou.!random|capitalize=.\n\n=spice:quests.FindaSite.typeOfDirections.$typeOfDirections.intro.!random|capitalize=.",

"=spice:quests.InteractWithAnObject.strangeplan.intro.!random=\n\n=spice:quests.InteractWithAnObject.strangeplan.comeClose.!random|capitalize= =spice:quests.InteractWithAnObject.strangeplan.myPlan.!random|capitalize=. =spice:quests.InteractWithAnObject.strangeplan.goTo.!random|capitalize=. No, I cannot tell you why. =spice:quests.FindaSpecificItem.personal.willYouDoIt.!random|capitalize= =spice:quests.InteractWithAnObject.strangeplan.IRewardYou.!random|capitalize=.\n\n=spice:quests.InteractWithAnObject.strangeplan.byThe_TellNoOne.!random|capitalize=.":
"=spice:quests.InteractWithAnObject.strangeplan.intro.!random=\n\n=spice:quests.InteractWithAnObject.strangeplan.comeClose.!random|capitalize= =spice:quests.InteractWithAnObject.strangeplan.myPlan.!random|capitalize=. =spice:quests.InteractWithAnObject.strangeplan.goTo.!random|capitalize=. No, non posso dirti perché. =spice:quests.FindaSpecificItem.personal.willYouDoIt.!random|capitalize= =spice:quests.InteractWithAnObject.strangeplan.IRewardYou.!random|capitalize=.\n\n=spice:quests.InteractWithAnObject.strangeplan.byThe_TellNoOne.!random|capitalize=.",

# ── Lore / flavor ──────────────────────────────────────────────────────────
"I ACCEPT YOUR OFFERING!\n\nThe sparking baetyl gives you =reward=!":
"ACCETTO LA TUA OFFERTA!\n\nIl betilo scintillante ti dona =reward=!",

"You read one of the few legible excerpts from =title|color:Y=:\n\n\"=sentence=\"":
"Leggi uno dei pochi estratti leggibili da =title|color:Y=:\n\n\"=sentence=\"",

"{{C|Editor's note:}} =note=\n\n":
"{{C|Nota del redattore:}} =note=\n\n",

"{{C|Author's note:}} =note=\n\n":
"{{C|Nota dell'autore:}} =note=\n\n",

"You violated the covenant of the water ritual and killed your bonded kith. You are cursed.\n\n":
"Hai violato il patto del rituale dell'acqua e ucciso il tuo kith legato. Sei maledetto.\n\n",

"Whenever you perform the water ritual with a new creature, you gain an extra =repBonus= reputation. If you install this implant after you treat with a creature for the first time, you gain =repBonus= reputation the next time you treat with them.\nReputation costs in the water ritual are reduced by =ritualCostReduction=%.\nYou may Proselytize =proselytizeLimitBonus.things:additional creature=.\nCompute power on the local lattice increases this implant's effectiveness.":
"Ogni volta che esegui il rituale dell'acqua con una nuova creatura, guadagni =repBonus= reputazione extra. Se installi questo impianto dopo aver trattato con una creatura per la prima volta, guadagni =repBonus= reputazione la prossima volta.\nCosti di reputazione nel rituale ridotti di =ritualCostReduction=%.\nPuoi Proselitizzare =proselytizeLimitBonus.things:additional creature= in più.\nLa potenza di calcolo sulla rete locale aumenta l'efficacia di questo impianto.",

# ── Description labels ─────────────────────────────────────────────────────
"\n{{K|Weight: =weight= lbs.}}":
"\n{{K|Peso: =weight= lbs.}}",

"\n\nGender: ":
"\n\nGenere: ",

"\n\nPhysical features: ":
"\n\nCaratteristiche fisiche: ",

"\nEquipped: ":
"\nEquipaggiamento: ",

# ── Opening story ──────────────────────────────────────────────────────────
"On the =day= of =month=, you arrive at the oasis-hamlet of {{green|Joppa}}, along the far rim of {{Y|Moghra'yi, the Great Salt Desert}}.\n\nAll around you, moisture farmers tend to groves of viridian watervine. There are huts wrought from rock salt and brinestalk.\n\nOn the horizon, {{r|Qud's}} jungles strangle chrome steeples and rusted archways to the earth. Further and beyond, the fabled {{C|Spindle}} rises above the fray and pierces the cloud-ribboned sky.":
"Nel =day= di =month=, giungi all'oasi-borgo di {{green|Joppa}}, lungo il lontano margine di {{Y|Moghra'yi, il Grande Deserto di Sale}}.\n\nIntorno, coltivatori di umidità curano boschetti di vitalba viridiana. Capanne forgiate da sale gemma e stelo di salamoia.\n\nAll'orizzonte, le giungle di {{r|Qud}} strangolano guglie cromate e archi arrugginiti verso terra. Oltre e più lontano, il leggendario {{C|Fuso}} si eleva sopra la mischia e penetra il cielo fasciato di nuvole.",

"On the =day= of =month=, you arrive at the village of {{g|=state.string:villageZeroName=}}.\n\nOn the horizon, {{r|Qud's}} jungles strangle chrome steeples and rusted archways to the earth. Further and beyond, the fabled {{C|Spindle}} rises above the fray and pierces the cloud-ribboned sky.":
"Nel =day= di =month=, giungi al villaggio di {{g|=state.string:villageZeroName=}}.\n\nAll'orizzonte, le giungle di {{r|Qud}} strangolano guglie cromate e archi arrugginiti verso terra. Oltre e più lontano, il leggendario {{C|Fuso}} si eleva sopra la mischia e penetra il cielo fasciato di nuvole.",

# ── Tombs / engravings ─────────────────────────────────────────────────────
"=spice:tombstones.intro.!random=\n\n=name=\n\nSuccumbed to glotrot.\n\n=stringgamestate:MarkOfDeath=":
"=spice:tombstones.intro.!random=\n\n=name=\n\nSoccombuto al glotrot.\n\n=stringgamestate:MarkOfDeath=",

"The shrine depicts a significant event from the life of the ancient sultan =sultanName=:\n\n=gospel=":
"Il santuario raffigura un evento significativo dalla vita dell'antico sultano =sultanName=:\n\n=gospel=",

"You add the following entry into the {{K|Annals of Qud}}.\n\n\"On the =date.day= of =date.month=, {{Y|=subject.basename|strip=}} became =positive.if:admired:despised= by =faction.formattedName= for =reason=.\"":
"Aggiungi la seguente voce negli {{K|Annali di Qud}}.\n\n\"Il =date.day= di =date.month=, {{Y|=subject.basename|strip=}} divenne =positive.if:ammirato:disprezzato= da =faction.formattedName= per =reason=.\"",

"{{cyan|Engraved: This item is engraved with a scene from the life of the ancient =sultanTerm= {{magenta|=sultan=}}:\n\n=engraving=}}\n":
"{{cyan|Inciso: Questo oggetto reca incisa una scena dalla vita dell'antico =sultanTerm= {{magenta|=sultan=}}:\n\n=engraving=}}\n",

"\n{{cyan|Painted: This item is painted with a scene from the life of the ancient =sultanTerm= {{magenta|=sultan=}}:\n\n=painting=}}\n":
"\n{{cyan|Dipinto: Questo oggetto reca dipinta una scena dalla vita dell'antico =sultanTerm= {{magenta|=sultan=}}:\n\n=painting=}}\n",

# ── Misc descriptions ──────────────────────────────────────────────────────
"Extradimensional: This item recently materialized in this dimension having inherited some properties from its home dimension, {{O|=dimensionName=}}.\n":
"Extradimensionale: Questo oggetto si è materializzato in questa dimensione ereditando proprietà dalla dimensione d'origine, {{O|=dimensionName=}}.\n",

"You start to metabolize the meal, gaining the following effect for the rest of the day:\n\n{{W|=effect.details=}}":
"Inizi a metabolizzare il pasto, ottenendo il seguente effetto per il resto del giorno:\n\n{{W|=effect.details=}}",

# ── Campfire / cooking ─────────────────────────────────────────────────────
"You preserved:\n\n=items.join:.\n=.":
"Hai conservato:\n\n=items.join:.\n=.",

"You preserved:\n\n=preserveItem=.":
"Hai conservato:\n\n=preserveItem=.",

"\n{{y|[up to =n= remaining]}}":
"\n{{y|[fino a =n= rimasti]}}",

"\n{{y|[0 remaining]}}":
"\n{{y|[0 rimasti]}}",

"You start to metabolize the meal, gaining the following effect for the rest of the day:\n\n{{W|=effect=}}":
"Inizi a metabolizzare il pasto, ottenendo il seguente effetto per il resto del giorno:\n\n{{W|=effect=}}",

"You start to metabolize the meal, gaining the following effect for the rest of the day:\n\n{{W|=messages.join:\n=}}":
"Inizi a metabolizzare il pasto, ottenendo il seguente effetto per il resto del giorno:\n\n{{W|=messages.join:\n=}}",

# ── Village ────────────────────────────────────────────────────────────────
"What a savory smell! Teach me to cook the favorite dish of =villageName=.\n":
"Che profumo saporito! Insegnami a cucinare il piatto preferito di =villageName=.\n",

"{{w|This book recounts a tale from the history of the village =villageName=.}}\n\n=story=":
"{{w|Questo libro narra un racconto dalla storia del villaggio di =villageName=.}}\n\n=story=",

"{{w|This book recounts a tale from the history of the village =villageName=.}}\n\n=stories.join:\n=":
"{{w|Questo libro narra un racconto dalla storia del villaggio di =villageName=.}}\n\n=stories.join:\n=",

# ── 2.0.212.22 new entries ─────────────────────────────────────────────────

# Achievement
'Unlocked =time.fullDate=': 'Sbloccato il =time.fullDate=',

# PickGameObjectLine/Screen
'{{G|[owned by you]}}': '{{G|[tuo]}}',
'take all': 'prendi tutto',
'store an item': 'riponi oggetto',

# CharacterStatusScreen
'Level: =level= ¯ HP: =hp=/=hpfull= ¯ XP: =xp=/=xpnextlevel= ¯ Weight: =weight=#': 'Liv.: =level= ¯ PF: =hp=/=hpfull= ¯ EXP: =xp=/=xpnextlevel= ¯ Peso: =weight=#',
'Attribute Points: {{=color=|=ap=}}': 'Punti Attributo: {{=color=|=ap=}}',
'MP: {{=color=|=mp=}}': 'PM: {{=color=|=mp=}}',
'=subject.mutationTerm|initUpper= Points: {{=color=|=mp=}}': 'Punti =subject.mutationTerm|initUpper=: {{=color=|=mp=}}',
'{{G|RANK =level=/10}}': '{{G|GRADO =level=/10}}',
'{{C|[Morphotype]}}': '{{C|[Morfotipo]}}',
'{{R|[Physical Defect]}}': '{{R|[Difetto Fisico]}}',
'{{r|[Mental Defect]}}': '{{r|[Difetto Mentale]}}',
'{{c|[Physical =subject.MutationTerm=]}}': '{{c|[=subject.MutationTerm= Fisica]}}',
'{{c|[Mental =subject.MutationTerm=]}}': '{{c|[=subject.MutationTerm= Mentale]}}',
'Your {{W|Compute Power (CP)}} scales the bonuses of certain compute-enabled items and cybernetic implants. Your base compute power is 0.': '{{W|Potenza di Calcolo (PC)}} aumenta i bonus di certi oggetti e impianti cibernetici. Potenza di calcolo base: 0.',
'Show Effects': 'Mostra Effetti',
'Buy =player.MutationTerm=': 'Acquista =player.MutationTerm=',
'ATTRIBUTES': 'ATTRIBUTI',
'MAIN ATTRIBUTES': 'ATTRIBUTI PRINCIPALI',

# TinkeringLine/Screen
"{{K|You don't have any schematics.}})": '{{K|Nessun schema disponibile.}})',
'<no applicable items>': '<nessun oggetto applicabile>',
'{{hotkey||[=commandKey:Toggle|strip=]}} switch to modifications': '{{hotkey||[=commandKey:Toggle|strip=]}} passa a modifiche',
'{{hotkey||[=commandKey:Toggle|strip=]}} switch to build': '{{hotkey||[=commandKey:Toggle|strip=]}} passa a costruzione',

# Embark Builder / Chargen
'You must make a selection before advancing.': "Seleziona un'opzione prima di procedere.",
"Error decoding build code - Required Mod '=requiredMod=' not found.": "Errore di decodifica - Mod necessaria '=requiredMod=' non trovata.",
'There is no valid last character to use.': 'Nessun personaggio recente valido.',
'World Seed: ': 'Seme del mondo: ',
'Enter world seed:': 'Inserisci seme del mondo:',

# GameMain
'Player': 'Giocatore',
'You quit.': 'Partita abbandonata.',
'Error finishing quest step ': 'Errore nel completamento del passo di missione ',
'No saved game exists.': 'Nessun salvataggio trovato.',
'Loading game': 'Caricamento partita',
"That save file appears to be corrupt, you can try to restore the backup in your save directory (=path=.sav.gz.bak) by removing the 'bak' file extension.": "Il file di salvataggio sembra corrotto. Prova a ripristinare il backup (=path=.sav.gz.bak) rimuovendo l'estensione '.bak'.",
'That save file is likely not loading because of a mod error from =mod= (=name=), make sure the correct mods are enabled or contact the mod author.': "Il salvataggio non si carica probabilmente a causa di un errore nella mod =mod= (=name=). Verifica le mod attive o contatta l'autore.",
"That save file looks like it's from an older save format revision (=version=). Sorry!\n\nYou can probably change to a previous branch in your game client and get it to load if you want to finish it off.": "Salvataggio da versione precedente del formato (=version=).\n\nProva a passare a una versione precedente del gioco per caricarlo.",
"That save file looks like it's from a newer save format revision (=version=).\n\nYou can probably change to a newer branch in your game client and get it to load if you want to finish it off.": "Salvataggio da versione più recente del formato (=version=).\n\nProva ad aggiornare il gioco per caricarlo.",
"There was a fatal exception attempting to save your game. Caves of Qud attempted to recover your prior save. You probably want to close the game and reload your most recent save. It'd be helpful to send the save and logs to support@freeholdgames.com": "Errore critico durante il salvataggio. Caves of Qud ha tentato di recuperare il salvataggio precedente. Chiudi il gioco e ricarica l'ultimo salvataggio. Invia salvataggio e log a support@freeholdgames.com",

# ChavvahSystem
'The roaming keter of Chavvah, Tree of Life': 'Il keter errante di Chavvah, Albero della Vita',
'You touch the chiming rock. White noise carries on a distant wind.': 'Tocchi la roccia tintinnante. Rumore bianco si propaga su un vento lontano.',
'You discover =note.text|initLowerIfArticle=!': 'Scopri =note.text|initLowerIfArticle=!',
'Chavvah roams out of feeling range. You are no longer attuned.': 'Chavvah si allontana fuori dalla portata dei sensi. Non sei più sintonizzato.',

# CheckpointingSystem
'You died.': 'Sei morto.',
'DEBUG: Do you really want to die?': 'DEBUG: Vuoi davvero morire?',
'View final messages': 'Visualizza messaggi finali',
'Reload from checkpoint': 'Ricarica dal checkpoint',
'Retire character': 'Ritira personaggio',
'Quit to main menu': 'Torna al menu principale',
"Type 'RETIRE' to confirm.": "Digita 'RITIRA' per confermare.",
'RETIRE': 'RITIRA',
'If you retire this character, your score will be recorded and your character will be lost. Are you sure you want to RETIRE THIS CHARACTER FOREVER?': 'Ritirando questo personaggio il punteggio verrà registrato e il personaggio andrà perduto. Confermi di voler RITIRARE DEFINITIVAMENTE QUESTO PERSONAGGIO?',
'Checkpointing enabled': 'Checkpoint abilitato',

# CodaSystem
'END GAME': 'FINE PARTITA',
'Leaving the village will end the game.\n\nType =prompt= to confirm.': 'Abbandonare il villaggio terminerà la partita.\n\nDigita =prompt= per confermare.',

# HolyPlaceSystem
'You feel a sense of holiness here.': 'Percepisci un senso di sacralità in questo luogo.',

# NorthSheva
"You can't travel in this environment.": "Non è possibile viaggiare in questo ambiente.",
"You can't land here.": "Non è possibile atterrare qui.",
'That stop is too ruined for the mover to land.': "La fermata è troppo in rovina per consentire l'atterraggio.",
'You cannot do that here.': 'Non è possibile farlo qui.',

# Reclamation Quest
'=questName=, attempt #=number=': '=questName=, tentativo n°=number=',

# Svardym Storm
'Your hear a swelling thpthp sound.': 'Odi un crescente suono thpthp.',
'The sky begins to darken.': 'Il cielo inizia a oscurarsi.',
'The thpthp sound wanes.': 'Il suono thpthp si affievolisce.',
'The sky begins to brighten.': 'Il cielo inizia a schiarirsi.',

# Scholar
'Wilderness Lore: Random': 'Conoscenza Naturale: Casuale',

# XRLUITradeUI
'=subject.Does:have= nothing to trade.': '=subject.Does:have= nulla da scambiare.',
"You can't understand =trader.the.name's|strip= explanation.": "Non riesci a comprendere la spiegazione di =trader.the.name's|strip=.",
'This item is too complex for =trader.the.name|strip= to identify.': '=trader.the.name|strip= non è in grado di identificare questo oggetto.',
'=trader.Does:identify= =object.the.name:long:notAsPossessed= as =object.a.name:asIfKnown=.': '=trader.Does:identify= =object.the.name:long:notAsPossessed= come =object.a.name:asIfKnown=.',
"=trader.Does:don't|strip= have the skill to identify artifacts.": "=trader.Does:don't|strip= non ha la competenza per identificare artefatti.",

# Search Input
'{{K|<search>}}': '{{K|<cerca>}}',
'Enter search text': 'Inserisci testo di ricerca',

# PickItem
'{{W|Select an item to store}}': '{{W|Seleziona oggetto da riporre}}',
'{{W|Select an item}}': '{{W|Seleziona un oggetto}}',
'=commandKey:Take All= {{Y|Take all}}': '=commandKey:Take All= {{Y|Prendi tutto}}',
'=commandKey:Store Items= {{Y|Store an item}}': '=commandKey:Store Items= {{Y|Riponi oggetto}}',
'<{{W|8}} to scroll up>': '<{{W|8}} per scorrere su>',
'<{{W|2}} to scroll down>': '<{{W|2}} per scorrere giù>',
'Taking =number.all.these= =number.isplural:objects:object= will put you over your weight limit. Are you sure you want to do it?': 'Raccogliere questi oggetti supererà il limite di peso. Procedere?',

# Popup ConsoleUI
'<up for more...>': '<su per altro...>',
'<down for more...>': '<giù per altro...>',
'[press space]': '[premi spazio]',
'[press {{W|space}}]': '[premi {{W|spazio}}]',
'[↑↓→← adjust,Enter or space to confirm]': '[↑↓→← regola, Invio o spazio per confermare]',
'[{{W|↑↓→←}} adjust, {{W|Enter}} or space to confirm]': '[{{W|↑↓→←}} regola, {{W|Invio}} o spazio per confermare]',
'Choose color': 'Scegli colore',
'[Enter to confirm]': '[Invio per confermare]',
'[{{W|Enter}} to confirm]': '[{{W|Invio}} per confermare]',
'{{y|[=commandKeyConsole:CmdDelete=] Accept}}': '{{y|[=commandKeyConsole:CmdDelete=] Accetta}}',
'{{y|=commandKeyConsole:Take All= Deselect All}}': '{{y|=commandKeyConsole:Take All= Deseleziona tutto}}',
'{{y|=commandKeyConsole:Take All= Select All}}': '{{y|=commandKeyConsole:Take All= Seleziona tutto}}',
'Select how many?': 'Quanti selezionare?',
'=preview= (no coloring)': '=preview= (senza colore)',
'[Yes] [No]': '[Sì] [No]',
'[{{W|Y}}es] [{{W|N}}o]': '[{{W|S}}ì] [{{W|N}}o]',
'[=commandKeyConsole:Accept=-Yes] [=commandKeyConsole:V Negative=-No] [=commandKeyConsole:Cancel=-Cancel]': '[=commandKeyConsole:Accept=-Sì] [=commandKeyConsole:V Negative=-No] [=commandKeyConsole:Cancel=-Annulla]',
'[Yes] [No] [ESC-Cancel]': '[Sì] [No] [ESC-Annulla]',
'[{{W|Y}}es] [{{W|N}}o] [{{W|ESC}}-Cancel]': '[{{W|S}}ì] [{{W|N}}o] [{{W|ESC}}-Annulla]',
'There =errorCount.ifPlural:were:was= =errorCount.things:error= while loading this =loadable=.': 'Si sono verificati =errorCount.things:errore= durante il caricamento di =loadable=.',
'Missing mods: ': 'Mod mancanti: ',
'Do you want to examine these errors in the Player.log?': 'Esaminare gli errori nel Player.log?',
'Loading Compat.xml': 'Caricamento di Compat.xml',
'{{W|[R]}} {{y|Retry}}': '{{W|[R]}} {{y|Riprova}}',
'{{W|[W]}} {{y|Workshop}}': '{{W|[W]}} {{y|Workshop}}',
'=modname= - {{R|Errors}}': '=modname= - {{R|Errori}}',
'{{W|Dependencies}}': '{{W|Dipendenze}}',
'{{W|Update Available}}': '{{W|Aggiornamento Disponibile}}',
'(... {{R|=number=}} more)': '(... {{R|=number=}} altri)',
'Automatically on your clipboard should you wish to forward it to =author=.': 'Copiato negli appunti. Invialo a =author= se lo desideri.',
'Automatically on your clipboard should you wish to forward it to the mod author.': "Copiato negli appunti. Invialo all'autore della mod se lo desideri.",
'Version mismatch': 'Versione incompatibile',
'Missing': 'Mancante',
'=modtitle= is missing one or more dependencies.': '=modtitle= ha una o più dipendenze mancanti.',
'{{W|=== Required ===}}': '{{W|=== Necessarie ===}}',
'{{W|=== Optional ===}}': '{{W|=== Facoltative ===}}',
'=modtitle= has a new version available: =version=.': 'Nuova versione di =modtitle= disponibile: =version=.',
'=== =modtitle= =version= Errors ===': '=== Errori =modtitle= =version= ===',
'=== =modtitle= Errors ===': '=== Errori =modtitle= ===',
'== Warnings ==': '== Avvisi ==',

# Journal
'Dimensions': 'Dimensioni',

# BuyRandomMutation
'Your type of creature may not buy =subject.mutationTerm|pluralize=.': 'Il tipo di creatura non può acquisire =subject.mutationTerm|pluralize=.',
"You don't have =cost= mutation points!": 'Non hai =cost= punti mutazione!',
'Are you sure you want to spend =cost= mutation points to buy a new =subject.mutationTerm=?': 'Spendere =cost= punti mutazione per acquisire nuova =subject.mutationTerm=?',

# QudAPISaves
'{{R|Corrupt info file}}': '{{R|File info corrotto}}',
'Total size: =size=mb': 'Dimensione totale: =size=mb',
'Level =level= =subtype= =gamemode=': 'Livello =level= =subtype= =gamemode=',
'=location=, =ingametime= turn =turn=': '=location=, =ingametime= turno =turn=',
'{{R|Older Version (=version=)}} =savename=': '{{R|Versione precedente (=version=)}} =savename=',
'There was a permission error while trying to access your save directory.': "Errore di permessi nell'accesso alla cartella dei salvataggi.",
'There was an error while trying to access your save directory.': "Errore nell'accesso alla cartella dei salvataggi.",
'Directory: =path=': 'Cartella: =path=',
"Caves of Qud will exit now since we cannot save games. Please check your directory's permissions.": 'Caves of Qud si chiuderà perché impossibile salvare. Controlla i permessi della cartella.',
'Error reading save location.': 'Errore nella lettura della posizione di salvataggio.',
'Quit': 'Esci',

# Biome creature roles/adjectives
'friend to fungi': 'amico dei funghi',
'{{r|qudzu}} symbiote': '{{r|qudzu}} simbiotico',
'web-toed': 'dalle zampe palmate',
'slimy-finned': 'dalle pinne viscide',
'slime-spitting': 'sputafango',
'kindlethumbed': 'accenditrice',
'firethumbed': 'ignifuoco',

# Loading status bars
'Loading Bodies.xml': 'Caricamento di Bodies.xml',
'Loading SparkingBaetyls.xml': 'Caricamento di SparkingBaetyls.xml',

# CreatureRegionSpice
'Time in =locale= has altered =pronouns.possessive= features -- =fragments.join:, = -- and given them =cast=.': 'Il tempo trascorso a =locale= ha alterato i tratti di =pronouns.possessive= -- =fragments.join:, = -- donando =cast=.',

# Roboticized
'{{c|mechanical}}': '{{c|meccanico}}',
"There is a low, persistent hum emanating outward.": "Un ronzio basso e persistente si propaga verso l'esterno.",

# MatterPhase
'solid': 'solido',
'gas': 'gas',
'plasma': 'plasma',

# Saving Throw
'disease onset': 'insorgenza malattia',
'{{rules|=bonus.signed=}} to saves vs. =type.saveBonusTypeDescription=': '{{rules|=bonus.signed=}} ai tiri salvezza vs. =type.saveBonusTypeDescription=',
'=bonus.signed= to saves vs. =type.saveBonusTypeDescription=': '=bonus.signed= ai tiri salvezza vs. =type.saveBonusTypeDescription=',

# StyledStatus
'Healthy': 'Integro',

# mutationbgone
'Choose a mutation for me to gobble up!': 'Scegli una mutazione che voglio divorare!',
'Huh? Get some mutations first if you want me to eat them!': 'Ottieni prima qualche mutazione se vuoi che le divori!',
"Didn't find that one. Try again?": 'Non trovata. Riprovare?',
'Om nom nom! =mutation.name= is gone! {{w|*belch*}}': 'Gnammm! =mutation.name= è scomparsa! {{w|*erutto*}}',

# ConversationDelegate
'=subject.Does:gain= =xp|rules= XP!': '=subject.Does:gain= =xp|rules= EXP!',
' {{K|-learned from =faction.the.name=}}': ' {{K|-appreso da =faction.the.name=}}',
'{{K|[End]}}': '{{K|[Fine]}}',
'{{W|[confirm =sanctuary= as a sanctuary option]}}': '{{W|[conferma =sanctuary= come opzione santuario]}}',
"=sanctuary|capitalize= =plural.if:are:is= now a sanctuary option for the slynth.": "=sanctuary|capitalize= è ora opzione santuario per lo slynth.",
'{{W|[Build Golem]}}': '{{W|[Costruisci Golem]}}',
'You touched the chiming rock and attuned to Chavvah, the Tree of Life.': 'Hai toccato la roccia tintinnante e ti sei sintonizzato con Chavvah, Albero della Vita.',
'{{M|[lesser victory]}}': '{{M|[vittoria minore]}}',
'{{g|[give artifact]}}': '{{g|[dai artefatto]}}',
'You have no artifacts to give.': 'Non hai artefatti da donare.',
'Choose an artifact to give.': 'Scegli un artefatto da donare.',
"You can't give that object.": "Non puoi donare quell'oggetto.",
"{{g|[Share secrets from Resheph's life]}}": "{{g|[Condividi segreti dalla vita di Resheph]}}",
'You do not have any unshared secrets about the life of Resheph.': 'Non hai segreti non condivisi sulla vita di Resheph.',
'Choose secrets about the life of Resheph to share.': 'Scegli segreti sulla vita di Resheph da condividere.',
'You muse over the =numShared.pluralize:secret= with =object.name|strip= and gain some insight.': 'Rifletti sui =numShared.pluralize:secret= con =object.name|strip= e acquisisci comprensione.',
'You gain {{C|=xp=}} XP.': 'Guadagni {{C|=xp=}} EXP.',
"You don't have a high enough reputation with =faction.the.name=.": 'Reputazione insufficiente con =faction.the.name=.',

# Asleep Effect
'=subject.Does:gently:shake= =object.the.name= awake.': '=subject.Does:gently:shake= =object.the.name= svegliandolo.',
"You can't figure out how to wake =object.the.name=.": 'Non riesci a capire come svegliare =object.the.name=.',

# Blaze_Tonic Effect
'{{blaze|blaze}} tonic': 'tonico {{blaze|blaze}}',
'Your stomach swells with a burning sensation.': 'Lo stomaco si gonfia con una sensazione bruciante.',
'The =tonic.description= burns out of your system.': '=tonic.description= brucia fuori dal sistema.',
'You start to cool off.': 'Inizi a raffreddarti.',
'Your mutant physiology reacts adversely to the tonic. You erupt into flames!': 'La fisiologia mutante reagisce negativamente al tonico. Esplodi in fiamme!',
'The tonics you ingested react adversely to each other. You erupt into flames!': 'I tonici ingeriti reagiscono negativamente tra loro. Esplodi in fiamme!',

# Blind Effect
'{{K|blind}}': '{{K|cieco}}',

# BlinkingTicSickness Effect
'{{B|acute blinking tic}}': '{{B|tic del teletrasporto acuto}}',
'{{B|blinking}}': '{{B|teletrasporto}}',

# BoostedImmunity Effect
'{{G|boosted immunity}}': '{{G|immunità potenziata}}',

# BoostStatistic Effect
'boosted =stat.name=': '=stat.name= potenziata',
'Your =stat.title= increases.': '=stat.title= aumenta.',
'Your =stat.title= decreases.': '=stat.title= diminuisce.',
'Your =stat.title= returns to normal': '=stat.title= torna alla normalità',

# BrainBrineCurse Effect
'You learn the skill =skill.name|color:C=!': 'Apprendi la tecnica =skill.name|color:C=!',
'You gained the mutation =mutation.name|color:G=!': 'Acquisisci la mutazione =mutation.name|color:G=!',
'Your mind begins to morph but the physiology of your brain restricts it.': 'La mente inizia a trasformarsi ma la fisiologia del cervello la limita.',
'You gained the defect =mutation.name|color:R=!': 'Acquisisci il difetto =mutation.name|color:R=!',
"You shake the water from your addled brain, but someone else's thoughts have already taken root.": "Scuoti l'acqua dal cervello confuso, ma i pensieri altrui hanno già attecchito.",

# Broken Effect
'{{r|broken}}': '{{r|rotto}}',
'*=subject.name:withTitles|strip= broken*': '*=subject.name:withTitles|strip= rotto*',
'[{{r|broken}}]': '[{{r|rotto}}]',
"You can't equip =object.the.name=, =object.itis= broken!": 'Impossibile equipaggiare =object.the.name=, è rotto!',

# Budding Effect
'{{r|budding}}': '{{r|in gemmazione}}',
'{{r|about to bud}}': '{{r|prossimo alla gemmazione}}',
'A grotesque protuberance swells from =subject.poss#back= as =subject.it.does:begin= to bud!': 'Una protuberanza grottesca gonfia da =subject.poss#back= mentre inizia la gemmazione!',
'A grotesque protuberance swells from =subject.the.name= as =subject.it.does:begin= to bud!': 'Una protuberanza grottesca gonfia da =subject.the.name= mentre inizia la gemmazione!',
'The grotesque protuberance on =subject.poss#back= subsides.': 'La protuberanza grottesca su =subject.poss#back= regredisce.',
'=subject.Poss:grotesque protuberance= subsides.': '=subject.Poss:protuberanza grottesca= regredisce.',

# Burrowed Effect
'{{w|burrowed}}': '{{w|sottoterra}}',
'=subject.Does:burrow= into the ground.': '=subject.Does:burrow= nel terreno.',
'You cannot do that while burrowed.': 'Impossibile farlo mentre si è sottoterra.',
'You cannot travel long distances while burrowed.': 'Impossibile viaggiare a lungo mentre si è sottoterra.',
'=subject.Does:are= forced to the surface.': '=subject.Does:are= respinto in superficie.',
'=subject.Does:emerge= from the ground.': '=subject.Does:emerge= dal terreno.',

# RealityStabilized
'=subject.The.name:notAsPossessed:includeAdjunctNoun= =subject.verb:shower= sparks everywhere.': '=subject.The.name:notAsPossessed:includeAdjunctNoun= =subject.verb:shower= scintille ovunque.',
"=user.The.name's= =subject.name:includeAdjunctNoun= =subject.verb:emit= a shower of sparks!": "=user.The.name's= =subject.name:includeAdjunctNoun= =subject.verb:emit= una pioggia di scintille!",
"=user.The.name's= =subject.name:includeAdjunctNoun= =subject.verb:shower= sparks everywhere.": "=user.The.name's= =subject.name:includeAdjunctNoun= =subject.verb:shower= scintille ovunque.",

# Liquid Glitching
"=subject.The.name's= mind starts to fluctuate in and out of coherence.": "La mente di =subject.The.name's= inizia a oscillare in preda all'incoerenza.",

# Combat miss messages
'{{r|=subject.Does:miss= with =weapon.the.name:withTitles:itsPossessor=!}} [=hitResult= vs. =dv=]': '{{r|=subject.Does:miss= con =weapon.the.name:withTitles:itsPossessor=!}} [=hitResult= vs. =dv=]',
'{{r|You miss!}} [=hitResult= vs. =dv=]': '{{r|Mancato!}} [=hitResult= vs. =dv=]',
'=subject.Does:miss= you with =weapon.the.name:withTitles:itsPossessor=! [=hitResult= vs. =dv=]': '=subject.Does:miss= con =weapon.the.name:withTitles:itsPossessor=! [=hitResult= vs. =dv=]',
'=subject.Does:miss= you! [=hitResult= vs. =dv=]': '=subject.Does:miss= il bersaglio! [=hitResult= vs. =dv=]',

# Cybernetics
"You can't remove =object.the.name:notAsPossessed=.": 'Impossibile rimuovere =object.the.name:notAsPossessed=.',

# LiquidVolume
'=subject.Does:collect= =transfer.things:dram= of =snapshotLiquidName= =subject.from.container.direction#volume==containers.ifAny: in ==containers.properAndList=.': '=subject.Does:collect= =transfer.things:dram= di =snapshotLiquidName= =subject.from.container.direction#volume==containers.ifAny: in ==containers.properAndList=.',

# IModification
"No modification by the name '=modName=' could be found.": "Nessuna modifica con nome '=modName=' trovata.",
"No blueprint by the name '=objectName=' could be found.": "Nessun progetto con nome '=objectName=' trovato.",

# ModLiquidCooled
' [{{=color=|empty}}]': ' [{{=color=|vuoto}}]',
' [empty]': ' [vuoto]',
'=subject.Does:are= already full of =volume.liquid.name=.': '=subject.Does:are= già pieno di =volume.liquid.name=.',
'You have no =liquid.name|strip= for =object.the.name=.': 'Non hai =liquid.name|strip= per =object.the.name=.',
'You dump the =volume.liquid.name= out of =object.the.name=.': 'Svuoti =volume.liquid.name= da =object.the.name=.',
'You=partial.if: partially:= fill =snapshotName= with =volume.liquid.name=.': 'Riempi=partial.if: parzialmente:= =snapshotName= con =volume.liquid.name=.',
'{{=liquid.color=|liquid-cooled}}': '{{=liquid.color=|a raffreddamento liquido}}',
'Supply =host.the.name= with how many drams of your =liquid.name|strip=? (max=equals==amount=)': 'Quanti sorsi di =liquid.name|strip= fornire a =host.the.name=? (max=equals==amount=)',
'You have no =liquid.name|strip= to supply =host.the.name= with.': 'Non hai =liquid.name|strip= da fornire a =host.the.name=.',
'=host.Does:have= no room for more =liquid.name|strip=.': '=host.Does:have= non può contenere altro =liquid.name|strip=.',
'=owner.Does:transfer= =amount.things:dram= of =liquid.name|strip= to =host.indefiniteForOthers#owner=.': '=owner.Does:transfer= =amount.things:dram= di =liquid.name|strip= a =host.indefiniteForOthers#owner=.',
"Liquid-cooled: This weapon's rate of fire is increased, but it requires pure water to function. When fired, there's a one in =chance= chance that 1 dram is consumed.": "A raffreddamento liquido: cadenza di fuoco aumentata, richiede acqua pura. A ogni sparo, 1 possibilità su =chance= di consumare 1 sorso.",
"Liquid-cooled: This weapon's rate of fire is increased by =fireBonus=, but =subject.it= requires =mustBePure.if:pure :==liquid.name|strip= to function. When fired, there's a one in =chance= chance that 1 dram is consumed.": "A raffreddamento liquido: cadenza di fuoco +=fireBonus=, richiede =mustBePure.if:puro :==liquid.name|strip=. A ogni sparo, 1 possibilità su =chance= di consumare 1 sorso.",
'=subject.Does:emit= a grinding noise.': '=subject.Does:emit= un rumore cigolante.',
'=subject.Does:are= =statusPhrase=.': '=subject.Does:are= =statusPhrase=.',

# ModMagnetized
'magnetized': 'magnetizzato',
'=subject.Does:are= not able to float right now.': '=subject.Does:are= non in grado di fluttuare.',
'Magnetized: This item floats around you.': 'Magnetizzato: oggetto fluttua intorno.',
'=subject.Does:fall= to the ground; you pick =subject.them= up.': '=subject.Does:fall= a terra; recuperi =subject.them=.',
'=subject.Does:fall= to the ground.': '=subject.Does:fall= a terra.',

# ModMasterwork
'{{Y|masterwork}}': '{{Y|capolavoro}}',
'{{rules|Masterwork: This weapon scores critical hits =bonus=% of the time instead of 5%.}}': '{{rules|Capolavoro: arma ottiene colpi critici nel =bonus=% dei casi invece del 5%.}}',

# ModMercurial
'{{Y|mercurial}}': '{{Y|mercuriale}}',
'Mercurial: Teleports the user to safety upon taking damage.': 'Mercuriale: teletrasporta in sicurezza quando si subiscono danni.',
'Mercurial: Teleports the user to safety upon taking damage (=chance=% chance).': 'Mercuriale: teletrasporta in sicurezza quando si subiscono danni (probabilità =chance=%).',

# ModMetered
'{{c|metered}}': '{{c|misurato}}',
'Metered: This item has a readout displaying its charge percentage.': 'Misurato: mostra percentuale di carica.',

# ModMorphogenetic
'{{m|morphogenetic}}': '{{m|morfogenetico}}',
'Morphogenetic: When powered and used to perform a successful, damaging hit, this weapon attempts to daze all other creatures of the same species as your target on the local map. Compute power on the local lattice increases the strength of this effect.': "Morfogenetico: con alimentazione attiva, dopo un colpo dannoso riuscito tenta di stordire tutte le creature della stessa specie del bersaglio sulla mappa. La potenza di calcolo locale amplifica l'effetto.",
'A weird=analgesic.if::, painful= shock reverbates through you.': 'Uno strano=analgesic.if::, doloroso= shock riverbera in tutto il corpo.',

# ModNanon
'{{K|nanon}}': '{{K|nanon}}',
'Nanon: This weapon has a chance to dismember on penetration.': "Nanon: l'arma ha probabilità di amputare in caso di penetrazione.",
'Nanon: =high=% chance to dismember on penetration': 'Nanon: =high=% di probabilità di amputare in caso di penetrazione',
'Nanon: =low=-=high=% chance to dismember on penetration': 'Nanon: =low=–=high=% di probabilità di amputare in caso di penetrazione',
'Nanon: =chance=% chance to dismember on penetration': 'Nanon: =chance=% di probabilità di amputare in caso di penetrazione',

# ModNav
'Nav: When powered and booted up, this item enhances navigation.': 'Nav: con alimentazione attiva potenzia la navigazione.',

# AnchorRoomTile
'Tomb-tethered!': 'Legato alla tomba!',

# Misc delegates / replacers
'You now have =total= feet of copper wire.': 'Ora hai =total= piedi di filo di rame.',
'=days.cardinal= =days.pluralize:day=': '=days.cardinal= =days.pluralize:day=',
'soon': 'presto',
'{{w|This rank}}:\n': '{{w|Questo grado}}:\n',
'\n\n{{w|Next rank}}:\n': '\n\n{{w|Grado successivo}}:\n',
'{{K|| Bit Cost |}}\n=coststring=': '{{K|| Costo in bit |}}\n=coststring=',
'-or-': '-o-',
'{{R|X}} =tinkereditem=': '{{R|X}} =tinkereditem=',

}


def strip_marker(v):
    return v.lstrip('▶').strip() if v else ''

def xml_escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def attr_escape(s):
    # Attribute values must encode newlines; XML parsers normalize them otherwise
    return xml_escape(s).replace('\n', '&#10;').replace('\r', '&#13;')

def xml_unescape(s):
    return s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#10;', '\n').replace('&#xA;', '\n')

def make_line(ctx, key, it_val, use_value_attr):
    ctx_part   = f' Context="{attr_escape(ctx)}"' if ctx else ''
    key_esc    = attr_escape(key)
    it_val_esc = xml_escape(it_val)
    if use_value_attr or '\n' in it_val:
        val_encoded = ('▶' + it_val_esc).replace('\n', '&#10;')
        return f'  <string{ctx_part} ID="{key_esc}" Value="{val_encoded}"/>\n'
    else:
        return f'  <string{ctx_part} ID="{key_esc}">▶{it_val_esc}</string>\n'

# Parse source: ordered unique entries + whether they use Value attr
src_root = ET.parse(SRC).getroot()
src_entries = []
src_seen = set()
for el in src_root.iter():
    k = el.get('ID') or el.get('Id') or el.get('id')
    if k and k not in src_seen:
        src_seen.add(k)
        v_raw = el.text or el.get('Value') or ''
        ctx   = el.get('Context') or ''
        uses_val_attr = (el.get('Value') is not None)
        src_entries.append((k, v_raw, ctx, uses_val_attr))

# Parse Italian: key → element
it_root = ET.parse(IT).getroot()
it_map = {}
for el in it_root.iter():
    k = el.get('ID') or el.get('Id') or el.get('id')
    if k and k not in it_map:
        v_raw = el.text or el.get('Value') or ''
        ctx   = el.get('Context') or ''
        uses_val_attr = (el.get('Value') is not None)
        it_map[k] = (v_raw, ctx, uses_val_attr)

# Build new Italian file
lines = []
lines.append("<?xml version='1.0' encoding='UTF-8'?>\n")
lines.append('<strings Lang="it" Encoding="utf-8">\n')

missing_count    = 0
translated_count = 0
copied_count     = 0

for key, src_raw, ctx, uses_val_attr in src_entries:
    if key in it_map:
        it_raw, it_ctx, it_uses_val = it_map[key]
        it_val = strip_marker(it_raw)
        lines.append(make_line(it_ctx or ctx, key, it_val, it_uses_val or uses_val_attr))
    else:
        missing_count += 1
        src_val = strip_marker(src_raw)
        if src_val in TRANS:
            it_val = TRANS[src_val]
            translated_count += 1
        else:
            it_val = src_val  # untranslated placeholder
            copied_count += 1
        lines.append(make_line(ctx, key, it_val, uses_val_attr))

lines.append('</strings>\n')

with open(IT, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Done. Inserted {missing_count} missing entries:")
print(f"  translated:  {translated_count}")
print(f"  copied as-is: {copied_count}")
print(f"Total lines written: {len(lines)}")

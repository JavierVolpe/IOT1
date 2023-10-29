# IOT1 - 1B4 - Kea


ID: 1
Kategori:
UI	Krav: 
Løsningen skal som minimum kunne fremvise lokation og batteridata via et online dashboard, med en opdateringsrate på minimum 2 opdateringer i minuttet.
	Prioritet: 1
Accepttest: 
Step 1) Testbrugeren ifører sig løsningens hardware del, og hardwareløsningen aktiveres.
Step 2) Indenfor 4 minutter bliver position og batteriniveau data præsenteret i et online dashboard. 
Step 3) Et stopur sættes i gang, og der måles hvor mange opdateringer dashboardet får over en periode på 5 minutter.

Vil der over perioden være 10 eller flere opdateringer, så vurderes kravet som bestået.
ID: 2
Kategori:
Power	Krav: 
Den kropsbårne løsning skal være batteridrevet, og skal have over 115 minutters batterilevetid.	Prioritet: 1
Accepttest:
Step 1) Testbrugeren ifører sig løsningens hardware del, og hardwareløsningen aktiveres.
Step 2) Et stopur sættes i gang, og testbrugeren påbegynder en træningssession på 2 x 45 minutter, med en 15 min pause i mellem.

Hvis løsningen stadig har over 10 % batteri ved afslutningen af forløbet på 115 min, så vurderes kravet at være opfyldt.
ID: 3
Kategori:
Connectivity	Krav: Løsningen skal være opkoblet til internettet, og være mobil.	Prioritet: 1
Accepttest:
Step 1) Løsningens hardware del placeres på en testbruger, aktiveres, og dashboardet observeres
Step 2) Testbrugeren går 1 km væk fra startpunktet og vender tilbage til startpunktet.

Hvis løsningen opretholder internetforbindelsen og ingen pakketab har gennem hele gåturen, vurderes kravet at være opfyldt.
ID: 4
Kategori:
Mechanical	Krav: Løsningens hardware del skal være kropsbåret, robust, og ikke være til fare for spiller under en fodboldkamp.	Prioritet: 1
Accepttest:
Step 1) Testbrugeren ifører sig løsningens hardware del, og hardwareløsningen aktiveres.
Step 2) Testbrugeren ligger sig ned på græsplæne og ruller rundt 10 gange.
Step 3) Testbrugeren bliver tacklet 10 gange

Hvis testbrugeren ikke oplever nogen gener, stammende fra løsningens hardware del, fra denne test, og at elektronikken ikke udviser tegn på skader, så vurderes kravet at være opfyldt.
ID: 5
Kategori:
Sensing	Krav: Løsningen skal kunne måle og visualisere brugerens position.	Prioritet: 1
Accepttest:
Step 1) Testbrugeren ifører sig løsningens hardware del, og hardwareløsningen aktiveres.
Step 2) Testbrugeren går i en cirkel med en diameter på 10 meter.
Step 3) Testbrugerens position visualiseres via dashboardet



Hvis dashboardet fremviser en cirkel, med en diameter på 10 meter (+/-3 meter), vurderes kravet at være bestået. 


ID8  

Kategori: Sensing 

Krav 

Løsningen skal afspille en lyd, hver gang en spiller løber 1kilometer, samt sende optælling af meter til Adafruit, med et interval på 100meter 

Prioritet: 1 

Accepttest:  

Step 1) Testbrugeren ifører sig løsningen hardware del, og hardwareløsningen aktiveres 

Step 2) Testbrugeren bevæger sig 1,1km 

Step 3) Observer om løsningen laver en lyd per kilometer og at dashboardet laver en optælling af meter i et interval af 100meter 

  

Opfyldt 1) 

Hvis løsningen afspiller en lyd indenfor 900 – 1100 meter, og dashboardet laver en optælling indenfor 90-110 meter, er kravet opfyldt 

 

Opfyldt 2)  

Hvis løsningen afspiller en lyd, og dashboardet laver en optælling med en nøjagtighed på +-10%, er kravet opfyldt 



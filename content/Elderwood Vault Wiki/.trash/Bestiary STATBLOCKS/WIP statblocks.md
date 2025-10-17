
```statblock
layout: Genesys2
name: Imperial Stormtrooper
monster: Imperial Stormtrooper
desc: Standard Imperial Canonfodder
qty: 1
image: https://static.wikia.nocookie.net/starwars/images/c/ca/Anovos_Stormtrooper.png/revision/latest/top-crop/width/360/height/360?cb=20160407220950
type: Adversary
soak: 5
wounds: 5
strain: 19
rdef: 0
mdef: 0
stats: [3,3,3,2,3,1]
athletics: 3
arcana: 4
knwgeo: 3

equipment:
  - name: Blaster Rifle
    desc: Ranged Heavy, Damage +9, Critical 3, Long Range, Stun
  - name: Light repeating blaster
    desc: Ranged Heavy, Damage +11, Critical 3, Long Range, Auto-fire, Cumbersome 4,
      Pierce 1, Weapon Sling.
  - name: Vibro Knife
    desc: Melee, Damage +4, Crit 2, Engaged, Pierce 2, Vicious 1
  - name: Frag Grenade
    desc: Ranged Light, Damage +8, Crit 4, Short Range, Blast 6, Limited Ammo 1
  - name: Extra Gear
    desc: Utility belt, Extra reloads, Stormtrooper armor, 2 frag grenades
```






####  PROPER STATBLOCK LAYOUT CODE
//Static Definitions

  

let icons = {

  "soak": 0x1F9FD,

  "wounds": 0x1FA78,

  "strain": 0x1F4A2,

  "rdef": 0x1F3F9,

  "mdef": 0x1F6E1,

  "def": 0x1F6E1,

};

  

let names = {

  "soak": "Soak",

  "wounds": "Wounds",

  "strain": "Strain",

  "rdef": "Ranged Def",

  "mdef": "Melee Def",

  "def": "Defense",

};

  

let diceprofIcon = "#Proficiency"

let diceabilityIcon = "#Ability"

let skillValues = [];

let characteristicsValues = [];

  

//Add skillValues.push() here

skillValues.push(monster.arcana, monster.athletics, monster.brawl, monster.charm, monster.coercion, monster.computers, monster.cool, monster.coordination, monster.deception, monster.discipline, monster.leadership, monster.mechanics, monster.medicine, monster.meleehvy, monster.meleelight, monster.negotiation, monster.perception, monster.piloting, monster.ranged, monster.resilience, monster.skulduggery, monster.stealth, monster.streetwise, monster.survival, monster.divine, monster.alchemy, monster.knwadv, monster.knwlore, monster.knwgeo, monster.knwforb, monster.primal, monster.verse, monster.runes, monster.riding);

//Add characteristicsValues.push() here

characteristicsValues.push(monster.stats[2],monster.stats[0], monster.stats[0], monster.stats[5],monster.stats[4], monster.stats[2], monster.stats[5], monster.stats[1], monster.stats[3], monster.stats[4], monster.stats[5], monster.stats[2], monster.stats[2], monster.stats[0], monster.stats[0], monster.stats[5], monster.stats[3], monster.stats[1], monster.stats[1], monster.stats[4], monster.stats[3], monster.stats[1], monster.stats[3], monster.stats[3], monster.stats[3], monster.stats[4], monster.stats[2], monster.stats[2], monster.stats[2], monster.stats[2], monster.stats[4], monster.stats[5], monster.stats[2], monster.stats[1]);

//Add skillLabels = here

let skillLabels = ["Arcana", "Athletics", "Brawl", "Charm", "Coercion", "Computers", "Cool", "Coordination", "Deception", "Discipline", "Leadership", "Mechanics", "Medicine", "Melee Heavy", "Melee Light", "Negotiation", "Perception", "Piloting", "Ranged", "Resilience", "Skulduggery", "Stealth", "Streetwise", "Survival", "Divine", "Alchemy", "Knowledge Adventuring", "Knowledge Lore", "Knowledge Geography", "Knowledge Forbidden", "Primal", "Verse", "Runes", "Riding"];

// Initial Dice Pools calculations.

  

let presentSkillsArray = [];

let presentCharacteristicsArray = [];

let presentLabelsArray = [];

let dicepoolArray = []; //initial Declaration

  

for (let x = 0; x < skillValues.length; x++) {

  let stat = skillValues[x];

  let label = skillLabels[x];

  let characteristic = characteristicsValues[x];

  let dicepoolElement = document.createElement('span');

  let qty = 0;

  

  // Skill level based on Qty if type minion

  if (typeof stat !== "undefined" ) { //&& (monster.type == "Minion" || monster.type == 'minion')

    // Skill cap at 5 (qty 6)

    if (monster.qty > 6) {

      qty = 6

    }

    else {

      qty = monster.qty

    }

    if  (monster.type == "Minion" || monster.type == 'minion') {

      stat = qty-1;

    }

  

    // Dice Pool Calculations

    let ability = Math.max(stat, characteristic) - Math.min(stat, characteristic);

    let prof = Math.min(stat, characteristic);

    //Div per Icon

    const profdice = document.createElement('span');

    const abilitydice = document.createElement('span');

    profdice.dataset.genesys = diceprofIcon + prof;

    abilitydice.dataset.genesys = diceabilityIcon + ability;

    // Add to Parallel Arrays

  

    dicepoolElement.appendChild(profdice);

    dicepoolElement.appendChild(abilitydice);

    dicepoolArray.push(dicepoolElement);

    presentSkillsArray.push(stat);

    presentCharacteristicsArray.push(characteristic);

    presentLabelsArray.push(label);

  }

}

  

//Stats (Wounds, Strain etc.) Calculation Function

  

let statWithIcon = (targetStat) => {

  if (targetStat == undefined || (targetStat in monster === false && targetStat !== "def") ) {

    return null;

  }

  

  let statValue = 0; //statValue starts at 0

  

  // Stats based on QTY for Minions, or Level if not.

  if ((monster.type == "Minion" || monster.type == "minion") && names[targetStat] == "Wounds") {

    statValue = monster[targetStat] * monster.qty;

  } else {

    statValue = monster[targetStat];

  }

  

  let icon = String.fromCodePoint(icons[targetStat]);

  let name = names[targetStat];

  

  let nameElement = document.createElement('strong');

  nameElement.id = "div_stat";

  nameElement.textContent = name;

  

  let iconElement = document.createElement('span');

  //iconElement.textContent = icon;

  iconElement.style.marginLeft = '5px';

  

  let statElement = document.createElement('span');

  statElement.id = "span_stat";

   // If to handle rdef/mdef differently (as a single object).

  if (targetStat == "def") {

    let mdeficon = String.fromCodePoint(icons["mdef"])

    let rdeficon = String.fromCodePoint(icons["rdef"])

    statElement.textContent = monster["rdef"] + "\u25CE"+ " | " + monster["mdef"] + "\uD83D\uDEE1";

  } else {

    statElement.textContent = statValue;

  }

  //statElement.textContent = statValue;

  

//DECREMENT BUTTON

  let decrementButton = document.createElement('button');

  decrementButton.textContent = '-';

  decrementButton.style.width = '15px'; // Set the width to 100 pixels

  decrementButton.style.height = '15px'; // Set the height to 15 pixels

  decrementButton.style.marginRight = '3px'; // Add right margin to create space

  decrementButton.style.lineHeight = '1'; //Center the +/- vertically.

  decrementButton.style.borderRadius = '20%';

  decrementButton.addEventListener('click', () => {

  

    statValue--;

    //Floor statValue at 1

    if (statValue < 1) {

      statValue = 1

    }

    statElement.textContent = statValue;

  

    if ((monster.type == "Minion" || monster.type == "minion") && names[targetStat] == "Wounds") {

      // Clear the children of outputElement after "rdefMdefContainer"

      let clearChildren = false;

      let childrenToRemove = [];

  

      Array.from(outputElement.children).forEach(child => {

        if (clearChildren) {

          childrenToRemove.push(child);

        }

        if (child.classList.contains('tapered-rule')) {

          clearChildren = true;

        }

      });

  

      childrenToRemove.forEach(child => {

        child.remove();

      });

  

      for (let i = 0; i < dicepoolArray.length; i++) {

        let stat = Math.ceil(statValue / monster.wounds)-1;

        //Cap Stat at 5

        if ( stat > 5 ) {

          stat = 5

        }

        let characteristic = presentCharacteristicsArray[i];

        let ability = Math.max(stat, characteristic) - Math.min(stat, characteristic);

        let prof = Math.min(stat, characteristic);

        //Put the Dice Quantities into a Span Property

        const profdice = document.createElement('span');

        const abilitydice = document.createElement('span');

        profdice.dataset.genesys = diceprofIcon + prof;

        abilitydice.dataset.genesys = diceabilityIcon + ability;

  

        //Put the Span in an Array

        let poolElement = document.createElement('span');

        poolElement.appendChild(profdice);

        poolElement.appendChild(abilitydice);

        dicepoolArray[i] = poolElement;

      }

  

      // Repopulate outputElement with updated content

      for (let x = 0; x < presentSkillsArray.length; x++) {

        let stat = presentSkillsArray[x];

        let label = presentLabelsArray[x];

        let characteristic = presentCharacteristicsArray[x];

  

        if (typeof stat !== "undefined" && (monster.type == "Minion" || monster.type == 'minion')) {

          let skillElement = document.createElement('strong');

          skillElement.textContent = label;

          let diceElement = document.createElement('span');

          diceElement = dicepoolArray[x];

  

          let dicecontainerElement = document.createElement('div');

          dicecontainerElement.id = "div_dicecontainer";

          dicecontainerElement.appendChild(skillElement);

          dicecontainerElement.appendChild(document.createTextNode(': '));

          dicecontainerElement.appendChild(diceElement);

          dicecontainerElement.appendChild(document.createElement('br'));

  

          outputElement.appendChild(dicecontainerElement);

      }

    }

  

  

  }

});

  

//MULTIPLE DECREMENT BUTTON

let decrementWholeButton = document.createElement('button');

decrementWholeButton.textContent = '-'+monster.wounds;

decrementWholeButton.style.width = '15px'; // Set the width to 100 pixels

decrementWholeButton.style.height = '15px'; // Set the height to 15 pixels

decrementWholeButton.style.marginRight = '3px'; // Add right margin to create space

decrementWholeButton.style.marginLeft = '3px'; // Add right margin to create space

decrementWholeButton.style.lineHeight = '1'; //Center the +/- vertically.

decrementWholeButton.style.borderRadius = '20%';

decrementWholeButton.addEventListener('click', () => {

  

  statValue = statValue-monster.wounds;

  //Floor statValue at 1

  if (statValue < 1) {

    statValue = 1

  }

  statElement.textContent = statValue;

  

  if ((monster.type == "Minion" || monster.type == "minion") && names[targetStat] == "Wounds") {

    // Clear the children of outputElement after "rdefMdefContainer"

    let clearChildren = false;

    let childrenToRemove = [];

  

    Array.from(outputElement.children).forEach(child => {

      if (clearChildren) {

        childrenToRemove.push(child);

      }

      if (child.classList.contains('tapered-rule')) {

        clearChildren = true;

      }

    });

  

    childrenToRemove.forEach(child => {

      child.remove();

    });

  

    for (let i = 0; i < dicepoolArray.length; i++) {

      let stat = Math.ceil(statValue / monster.wounds)-1;

      //Cap Stat at 5

      if ( stat > 5 ) {

        stat = 5

      }

      let characteristic = presentCharacteristicsArray[i];

      let ability = Math.max(stat, characteristic) - Math.min(stat, characteristic);

      let prof = Math.min(stat, characteristic);

      //Put the Dice Quantities into a Span Property

      const profdice = document.createElement('span');

      const abilitydice = document.createElement('span');

      profdice.dataset.genesys = diceprofIcon + prof;

      abilitydice.dataset.genesys = diceabilityIcon + ability;

  

      //Put the Span in an Array

      let poolElement = document.createElement('span');

      poolElement.appendChild(profdice);

      poolElement.appendChild(abilitydice);

      dicepoolArray[i] = poolElement;

    }

  

    // Repopulate outputElement with updated content

    for (let x = 0; x < presentSkillsArray.length; x++) {

      let stat = presentSkillsArray[x];

      let label = presentLabelsArray[x];

      let characteristic = presentCharacteristicsArray[x];

  

      if (typeof stat !== "undefined" && (monster.type == "Minion" || monster.type == 'minion')) {

        let skillElement = document.createElement('strong');

        skillElement.textContent = label;

        let diceElement = document.createElement('span');

        diceElement = dicepoolArray[x];

  

        let dicecontainerElement = document.createElement('div');

        dicecontainerElement.id = "div_dicecontainer";

        dicecontainerElement.appendChild(skillElement);

        dicecontainerElement.appendChild(document.createTextNode(': '));

        dicecontainerElement.appendChild(diceElement);

        dicecontainerElement.appendChild(document.createElement('br'));

  

        outputElement.appendChild(dicecontainerElement);

    }

  }

}

});

  

//INCREMENT BUTTON

  let incrementButton = document.createElement('button');

  incrementButton.textContent = '+';

  incrementButton.style.width = '15px'; // Set the width to 100 pixels

  incrementButton.style.height = '15px'; // Set the height to 15 pixels

  incrementButton.style.marginLeft = '3px'; // Add left margin to create space

  incrementButton.style.lineHeight = '1'; //Center the +/- vertically.

  incrementButton.style.borderRadius = '20%';

  incrementButton.addEventListener('click', () => {

    statValue++;

    //Cap statValue at wounds threshhold

    if (statValue > (monster[targetStat] * monster.qty)) {

      statValue = (monster[targetStat] * monster.qty)

    }

    statElement.textContent = statValue;

  

    if ((monster.type == "Minion" || monster.type == "minion") && names[targetStat] == "Wounds") {

      // Clear the children of outputElement after "rdefMdefContainer"

      let clearChildren = false;

      let childrenToRemove = [];

  

      Array.from(outputElement.children).forEach(child => {

        if (clearChildren) {

          childrenToRemove.push(child);

        }

        if (child.classList.contains('tapered-rule')) {

          clearChildren = true;

        }

      });

  

      childrenToRemove.forEach(child => {

        child.remove();

      });

  

      // Recalculate Dice Pools

      for (let i = 0; i < dicepoolArray.length; i++) {

        let stat = Math.ceil(statValue / monster.wounds)-1;

        // Cap Stat at 5

        if ( stat > 5 ) {

          stat = 5

        }

        let characteristic = presentCharacteristicsArray[i];

        let ability = Math.max(stat, characteristic) - Math.min(stat, characteristic);

        let prof = Math.min(stat, characteristic);

        //Put the Dice Quantities into a Span Property

        const profdice = document.createElement('span');

        const abilitydice = document.createElement('span');

        profdice.dataset.genesys = diceprofIcon + prof;

        abilitydice.dataset.genesys = diceabilityIcon + ability;

  

        //Put the Span in an Array

        let poolElement = document.createElement('span');

        poolElement.appendChild(profdice);

        poolElement.appendChild(abilitydice);

        dicepoolArray[i] = poolElement;

      }

  

      // Repopulate outputElement with updated content

      for (let x = 0; x < presentSkillsArray.length; x++) {

        let stat = presentSkillsArray[x];

        let label = presentLabelsArray[x];

        let characteristic = presentCharacteristicsArray[x];

  

        if (typeof stat !== "undefined" && (monster.type == "Minion" || monster.type == 'minion')) {

          let skillElement = document.createElement('strong');

          skillElement.textContent = label;

          let diceElement = document.createElement('span');

          diceElement = dicepoolArray[x];

  

          let dicecontainerElement = document.createElement('div');

          dicecontainerElement.id = "div_dicecontainer";

          dicecontainerElement.appendChild(skillElement);

          dicecontainerElement.appendChild(document.createTextNode(': '));

          dicecontainerElement.appendChild(diceElement);

          dicecontainerElement.appendChild(document.createElement('br'));

  

          outputElement.appendChild(dicecontainerElement);

        }

      }

    }

  });

  

  //MULTIPLE INCREMENT BUTTON

  let incrementWholeButton = document.createElement('button');

  incrementWholeButton.textContent = '+'+monster.wounds;

  incrementWholeButton.style.width = '15px'; // Set the width to 100 pixels

  incrementWholeButton.style.height = '15px'; // Set the height to 15 pixels

  incrementWholeButton.style.marginLeft = '3px'; // Add left margin to create space

  incrementWholeButton.style.marginRight = '3px'; // Add left margin to create space

  incrementWholeButton.style.lineHeight = '1'; //Center the +/- vertically.

  incrementWholeButton.style.borderRadius = '20%';

  incrementWholeButton.addEventListener('click', () => {

    statValue = statValue+monster.wounds;

    //Cap statValue at wounds threshhold

    if (statValue > (monster[targetStat] * monster.qty)) {

      statValue = (monster[targetStat] * monster.qty)

    }

    statElement.textContent = statValue;

  

    if ((monster.type == "Minion" || monster.type == "minion") && names[targetStat] == "Wounds") {

      // Clear the children of outputElement after "rdefMdefContainer"

      let clearChildren = false;

      let childrenToRemove = [];

  

      Array.from(outputElement.children).forEach(child => {

        if (clearChildren) {

          childrenToRemove.push(child);

        }

        if (child.classList.contains('tapered-rule')) {

          clearChildren = true;

        }

      });

  

      childrenToRemove.forEach(child => {

        child.remove();

      });

  

      // Recalculate Dice Pools

      for (let i = 0; i < dicepoolArray.length; i++) {

        let stat = Math.ceil(statValue / monster.wounds)-1;

        // Cap Stat at 5

        if ( stat > 5 ) {

          stat = 5

        }

        let characteristic = presentCharacteristicsArray[i];

        let ability = Math.max(stat, characteristic) - Math.min(stat, characteristic);

        let prof = Math.min(stat, characteristic);

        //Put the Dice Quantities into a Span Property

        const profdice = document.createElement('span');

        const abilitydice = document.createElement('span');

        profdice.dataset.genesys = diceprofIcon + prof;

        abilitydice.dataset.genesys = diceabilityIcon + ability;

  

        //Put the Span in an Array

        let poolElement = document.createElement('span');

        poolElement.appendChild(profdice);

        poolElement.appendChild(abilitydice);

        dicepoolArray[i] = poolElement;

      }

  

      // Repopulate outputElement with updated content

      for (let x = 0; x < presentSkillsArray.length; x++) {

        let stat = presentSkillsArray[x];

        let label = presentLabelsArray[x];

        let characteristic = presentCharacteristicsArray[x];

  

        if (typeof stat !== "undefined" && (monster.type == "Minion" || monster.type == 'minion')) {

          let skillElement = document.createElement('strong');

          skillElement.textContent = label;

          let diceElement = document.createElement('span');

          diceElement = dicepoolArray[x];

  

          let dicecontainerElement = document.createElement('div');

          dicecontainerElement.id = "div_dicecontainer";

          dicecontainerElement.appendChild(skillElement);

          dicecontainerElement.appendChild(document.createTextNode(': '));

          dicecontainerElement.appendChild(diceElement);

          dicecontainerElement.appendChild(document.createElement('br'));

  

          outputElement.appendChild(dicecontainerElement);

        }

      }

    }

  });

  

//Build Individual Stat Rows

  let statcontainerElement = document.createElement('div');

  statcontainerElement.id = "div_statcontainer";

  let buttoncontainerElement = document.createElement('div');

  buttoncontainerElement.id = "div_button";

  let decreaseButtons = document.createElement('div');

  decreaseButtons.id = "decreasebuttons"

  let increaseButtons = document.createElement('div');

  increaseButtons.id = "increasebuttons"

  statcontainerElement.appendChild(nameElement);

  //statcontainerElement.appendChild(document.createTextNode(' '));

  //statcontainerElement.appendChild(iconElement);

  //statcontainerElement.appendChild(document.createTextNode(' : '));

  if ((targetStat == "wounds" || targetStat == "strain") && (monster.type == "Minion" || monster.type == 'minion')) {

    decreaseButtons.appendChild(decrementWholeButton);

    decreaseButtons.appendChild(decrementButton);

    buttoncontainerElement.appendChild(decreaseButtons);

  

  }

  buttoncontainerElement.appendChild(statElement);

  if ((targetStat == "wounds" || targetStat == "strain") && (monster.type == "Minion" || monster.type == 'minion')) {

    increaseButtons.appendChild(incrementButton);

    increaseButtons.appendChild(incrementWholeButton);

    buttoncontainerElement.appendChild(increaseButtons);

  }

    statcontainerElement.appendChild(buttoncontainerElement);

  /*

  if (targetStat == "rdef" || targetStat == "soak" || (targetStat == "wounds" && monster.type !== "Minion" && monster.type !== 'minion' && monster.type !== "Rival" && monster.type !== "rival") ) {

    //let separatorElement = document.createElement('strong');

    //separatorElement.textContent = ' | ';

    //statcontainerElement.appendChild(separatorElement);

  }

*/

  //statcontainerElement.style.whiteSpace = 'pre'; // Apply CSS to preserve white spaces

  //statcontainerElement.style.display = 'flex'; // Set display property to flex

  //statcontainerElement.style.alignItems = 'center'; //Align all objects in div vertically center to the div

  

  return statcontainerElement;

};

  

// Render Stats into div

  

let outputElement = document.createElement('div');

outputElement.id = "div_output"

  

/* OLD SCRIPT

// Create a separate container for "soak" and "wounds" elements

let soakWoundsContainer = document.createElement('div');

soakWoundsContainer.id = "div_soakWoundsContainer"

soakWoundsContainer.style.display = 'flex'; // Set display property to flex

soakWoundsContainer.style.justifyContent = 'center';

soakWoundsContainer.appendChild(statWithIcon("soak"));

soakWoundsContainer.appendChild(statWithIcon("wounds"));

if (monster.type !== "undefined" && (monster.type !== "Minion" && monster.type !== "minion" && monster.type !== "Rival" && monster.type !== "rival")) {

  soakWoundsContainer.appendChild(statWithIcon("strain"));

}

outputElement.appendChild(soakWoundsContainer);

*/

  

// Create a separate container for "soak" and "wounds" elements

let soakContainer = document.createElement('div');

soakContainer.id = "div_soak"

let woundsContainer = document.createElement('div');

woundsContainer.id = "div_wounds"

let strainContainer = document.createElement('div');

strainContainer.id = "div_strain"

let allStatsContainer = document.createElement('div');

allStatsContainer.id = "div_allstats"

  

soakContainer.appendChild(statWithIcon("soak"));

woundsContainer.appendChild(statWithIcon("wounds"));

if (monster.type !== "undefined" && (monster.type !== "Minion" && monster.type !== "minion" && monster.type !== "Rival" && monster.type !== "rival")) {

  strainContainer.appendChild(statWithIcon("strain"));

}

  

allStatsContainer.appendChild(soakContainer);

allStatsContainer.appendChild(woundsContainer);

allStatsContainer.appendChild(strainContainer);

  

// Create a separate container for "rdef" and "mdef" elements

let rdefMdefContainer = document.createElement('div');

rdefMdefContainer.id = "div_rdefMdefContainer"

//rdefMdefContainer.style.display = 'flex'; // Set display property to flex

//rdefMdefContainer.style.justifyContent = 'center';

rdefMdefContainer.appendChild(statWithIcon("def"));

  

if (monster.rdef > 0 || monster.mdef > 0) {

  allStatsContainer.appendChild(rdefMdefContainer);

}

outputElement.appendChild(allStatsContainer);

  

let lineElement = document.createElement('div');

lineElement.id = "div_line"

lineElement.classList.add('tapered-rule');

outputElement.appendChild(lineElement);

  

// Render Dice Pools per Skill - If monster type is minion, exclude Skill level

for (let x = 0; x < presentSkillsArray.length; x++) {

  let stat = presentSkillsArray[x];

  let label = presentLabelsArray[x];

  if (typeof stat !== "undefined" ) { //&& (monster.type == "Minion" || monster.type == 'minion')

    let statElement = document.createElement('span');

    statElement.textContent = '('+stat+')';

    statElement.style.marginRight = '5px'; 

    let skillElement = document.createElement('strong');

    skillElement.textContent = label;

    //skillElement.style.marginRight = '5px';

    let diceElement = document.createElement('span');

    diceElement = dicepoolArray[x];

  

    let dicecontainerElement = document.createElement('div');

    dicecontainerElement.id = "div_dicecontainer";

    dicecontainerElement.appendChild(skillElement);

    dicecontainerElement.appendChild(document.createTextNode(': '));

  

    if (monster.type !== "Minion" && monster.type !== "minion") {

      dicecontainerElement.appendChild(statElement);

    }

    dicecontainerElement.appendChild(diceElement);

    dicecontainerElement.appendChild(document.createElement('br'));

    outputElement.appendChild(dicecontainerElement);

  

  }

}

  

//outputElement.style.width = '100%'

return outputElement;

 
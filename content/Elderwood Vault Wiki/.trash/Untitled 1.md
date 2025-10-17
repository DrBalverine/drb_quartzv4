# **Bandit**

**Type:** Minion  
**Species:** Human  
**Threat Level:** Low  

## **Characteristics**
- **Brawn:** `= this.brawn`  
- **Agility:** `= this.agility`  
- **Intellect:** `= this.intellect`  
- **Cunning:** `= this.cunning`  
- **Willpower:** `= this.willpower`  
- **Presence:** `= this.presence`  

## **Skills**
- **Melee (Light):** `= this.melee_light`  
- **Ranged (Light):** `= this.ranged_light`  
- **Stealth:** `= this.stealth`  
- **Skulduggery:** `= this.skulduggery`  

## **Combat Stats**
- **Soak:** `= this.soak`  
- **Wounds Threshold:** `= this.wounds_threshold`  
- **Defense (Melee/Ranged):** `= this.defense_melee` / `= this.defense_ranged`  

## **Abilities & Talents**
- **Strength in Numbers:** Gains +1 soak per additional minion in the group.  
- **Dirty Fighting:** Upgrades one ability die (`#GenesysAbility`) to a proficiency die (`#GenesysProficiency`) when attacking a surprised target.  

## **Equipment**
- **Rusty Sword** – Damage: 5, Critical: 3, Range: Engaged, Special: None  
- **Throwing Knife** – Damage: 4, Critical: 4, Range: Short, Special: Thrown  
- **Tattered Leather Armor** – Defense: 0, Soak: 1  

## **Dice Pool Calculation**
```dataview
TABLE 
  melee_light AS "Melee (Light) Ranks", 
  agility AS "Agility",
  (max(agility, melee_light) - min(agility, melee_light)) AS "Upgrades"
FROM #GenesysAdversary
WHERE file.name = this.file.name
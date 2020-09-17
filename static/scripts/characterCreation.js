let totalAttributes = 0;
let unassignedAttributes = 0;
let pilotAttributes = 0;
let fighterAttributes = 0;
let merchantAttributes = 0;
let engineerAttributes = 0;

function changePoints(difficulty) {
    switch(difficulty) {
        case "Easy":
            totalAttributes = 16;
            break;
        case "Medium":
            totalAttributes = 12;
            break;
        case "Hard":
            totalAttributes = 8;
            break;
        default:
            totalAttributes = 0;
            break;
    }
    unassignedAttributes = totalAttributes;
    pilotAttributes = 0;
    fighterAttributes = 0;
    merchantAttributes = 0;
    engineerAttributes = 0;
    updateAllAttributes();
}
function decrement(skill) {
    event.preventDefault();
    switch(skill) {
        case "pilot":
            if (pilotAttributes > 0) {
                pilotAttributes--;
                unassignedAttributes++;
            }
            break;
        case "fighter":
            if (fighterAttributes > 0) {
                fighterAttributes--;
                unassignedAttributes++;
            }
            break;
        case "merchant":
            if (merchantAttributes > 0) {
                merchantAttributes--;
                unassignedAttributes++;
            }
            break;
        case "engineer":
            if (engineerAttributes > 0) {
                engineerAttributes--;
                unassignedAttributes++;
            }
            break;
    }
    updateAllAttributes();
}

function increment(skill) {
    event.preventDefault();
    let changedAttribute;
    switch(skill) {
        case "pilot":
            if (pilotAttributes <= totalAttributes && 
                (unassignedAttributes + pilotAttributes + fighterAttributes + merchantAttributes + engineerAttributes) <= totalAttributes  && 
                unassignedAttributes > 0) {
                pilotAttributes++;
                unassignedAttributes--;
            }
            break;
        case "fighter":
                if (fighterAttributes <= totalAttributes && 
                    (unassignedAttributes + pilotAttributes + fighterAttributes + merchantAttributes + engineerAttributes) <= totalAttributes && 
                    unassignedAttributes > 0) {
                    fighterAttributes++;
                    unassignedAttributes--;
                }
            break;
        case "merchant":
                if (merchantAttributes <= totalAttributes && 
                    (unassignedAttributes + pilotAttributes + fighterAttributes + merchantAttributes + engineerAttributes) <= totalAttributes && 
                    unassignedAttributes > 0) {
                    merchantAttributes++;
                    unassignedAttributes--;
                }
            break;
        case "engineer":
                if (engineerAttributes <= totalAttributes && 
                    (unassignedAttributes + pilotAttributes + fighterAttributes + merchantAttributes + engineerAttributes) <= totalAttributes && 
                    unassignedAttributes > 0) {
                    engineerAttributes++;
                    unassignedAttributes--;
                }
            break;
        default:
            break;
    }
    updateAllAttributes();
}

function updateAllAttributes() {
    document.getElementById("Pilot").value = pilotAttributes;
    document.getElementById("Fighter").value = fighterAttributes;
    document.getElementById("Merchant").value = merchantAttributes;
    document.getElementById("Engineer").value = engineerAttributes;
    document.getElementById("unassigned").innerHTML = unassignedAttributes;
}

function checkSubmit() {
    event.preventDefault();
    if (unassignedAttributes == 0 && totalAttributes != 0 && document.getElementById("name").value != "") {
        document.creation.submit();
    } else if (totalAttributes == 0) {
        alert("Pick a difficulty");
    } else if (document.getElementById("name").value == "") {
        alert("Character Name is blank")
    } else {
        alert("There is still " + unassignedAttributes + " unassigned skill points");
    }

}
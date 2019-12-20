window.onload = doOnLoad;
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev,val) {
    ev.dataTransfer.setData(val, ev.target.id);
	
	for (var i=1; i<15;i++){
		var elemnt=document.getElementById('div'+i);
		if (elemnt != null){
			elemnt.style.backgroundColor = "#fff";
		}
		var elemnt=document.getElementById('div_'+i);
		if (elemnt != null){
			elemnt.style.backgroundColor = "#fff";
		}
		var elemnt=document.getElementById('div__'+i);
		if (elemnt != null){
			elemnt.style.backgroundColor = "#fff";
		}
	}
}

function drop(ev,val) {
    ev.preventDefault();
	
    var data = ev.dataTransfer.getData(val);
	
	var elementtodrop;
	if (data!=''){
		elementtodrop=document.getElementById(data);
		
		ev.target.appendChild(document.getElementById(data));
		ev.target.style.backgroundColor = "#C4F371";
	}else{
		ev.target.style.backgroundColor = "#F39171";
		
	}
   
}
function validateDragDrop(formname){
	
	for (var i=1; i<15;i++){
		var elemnt=document.getElementById('div'+i);
		var elemnt1=document.getElementById('div_'+i);
		var elemnt2=document.getElementById('div__'+i);
		var elemntdrag=document.getElementById('drag'+i);
		var elemntdrag1=document.getElementById('drag_'+i);
		var elemntdrag2=document.getElementById('drag__'+i);
		if (elemnt != null){
			elemnt.style.backgroundColor = "#C4F371";
			if( elemntdrag != null)
				elemnt.appendChild(elemntdrag);
		}
		if (elemnt1 != null){
			elemnt1.style.backgroundColor = "#C4F371";
			if( elemntdrag1 != null)
				elemnt1.appendChild(elemntdrag1);
		}
		if (elemnt2 != null){
			elemnt2.style.backgroundColor = "#C4F371";
			if( elemntdrag2 != null)
				elemnt2.appendChild(elemntdrag2);
		}
		
	}
	document.getElementById("divok").style.display = "block";
	if (formname=='L1_q3'  ){
		
		document.getElementById("drag8").style.backgroundColor = "#f3f17d";
		document.getElementById("drag9").style.backgroundColor = "#f3f17d";
		document.getElementById("drag10").style.backgroundColor = "#f3f17d";
		document.getElementById("drag11").style.backgroundColor = "#f3f17d";
		document.getElementById("drag12").style.backgroundColor = "#f3f17d";
		document.getElementById("drag13").style.backgroundColor = "#f3f17d";
		}
}
function validateFormRadio(formname) {
    var formObj = window.document.forms[formname];
    var elementlength=formObj.elements.length;
	var	valchecked = formObj.L.value;
    var res_text="";
	
	if (formname == 'L1_q3'){
		correctanswer=2;
    }else if (formname == 'L1_q4' || formname == 'L5_q2'){
		correctanswer=0;
	}else if (formname == 'L2_q1' || formname == 'L2_q2' ||formname == 'L2_q3'){
		correctanswer=1;
	} 
	
	if ( valchecked==correctanswer){
		document.getElementById("r"+valchecked).style.backgroundColor = "#C4F371";
		document.getElementById("feed"+valchecked).style.display = "block";
		res_text="Yes, you are right. Your answer is correct.";
	}else{
		document.getElementById("r"+valchecked).style.backgroundColor = "#F39171";
		document.getElementById("feed"+valchecked).style.display = "block";
		res_text="Your answer is incorrect.";
	}
	document.getElementById("L").setAttribute("disabled", "disabled");
	document.getElementById("a_L").style.backgroundColor = "#FADD8F";
	document.getElementById("a_L").style.fontSize = "12pt";
	document.getElementById("a_L").innerHTML=res_text;
	document.getElementById("check").disabled = true; 
	document.getElementById("check").setAttribute("disabled", "disabled");
	document.getElementById("check").style.backgroundColor = "#ebebeb";
}
function validateFormChecks2(formname) {
    var formObj = window.document.forms[formname];
    var elementlength=formObj.elements.length;
    
	var correctanswer=[];
	
	if (formname == 'L3_q1'){
		correctanswer=[false,false,true,true]
	}else if (formname == 'L3_q2'){
		correctanswer=[true,true,true,true,true,true,false,false,false]
	}else if (formname == 'L5_q1'){
		correctanswer=[false,true,true,true,false]
	}
	for( i=0;  i  < elementlength ; i++ ) {
		if(formObj.elements[i].type=="checkbox" ){
			if (formObj.elements[i].checked && correctanswer[i]==true ){
				document.getElementById("L_row"+i).style.backgroundColor = "#C4F371";
				document.getElementById("feed"+i).style.backgroundColor = "#f7f5be;";
				document.getElementById("feed"+i).style.display = "block";
				document.getElementById("feed_"+i).style.display = "block";
				
			
			}else if (formObj.elements[i].checked && correctanswer[i]==false){
				document.getElementById("L_row"+i).style.backgroundColor = "#F39171";
				document.getElementById("feed"+i).style.backgroundColor = "#F8C5B4;";
				document.getElementById("feed"+i).style.display = "block";
				document.getElementById("feed_"+i).style.display = "block";
				
			}		
        }
    }
	
	if (formname == 'L3_q1'){
		if (formObj.elements.L_2.checked && formObj.elements.L_3.checked && !formObj.elements.L_0.checked && !formObj.elements.L_1.checked ){
			document.getElementById("a_Lr").style.display = "block";
			document.getElementById("a_Lr").style.backgroundColor = "#FADD8F";
			document.getElementById("a_Lr").style.fontSize = "12pt";
		}else if(formObj.elements.L_2.checked || formObj.elements.L_3.checked){
			document.getElementById("a_Lr1").style.display = "block";
			document.getElementById("a_Lr1").style.backgroundColor = "#FADD8F";
			document.getElementById("a_Lr1").style.fontSize = "12pt";
		}else {
			document.getElementById("a_Lw").style.display = "block";
			document.getElementById("a_Lw").style.backgroundColor = "#FADD8F";
			document.getElementById("a_Lw").style.fontSize = "12pt";
		}
	}else if (formname == 'L3_q2'){
			if (formObj.elements.L_0.checked && formObj.elements.L_1.checked && formObj.elements.L_2.checked && formObj.elements.L_3.checked  && formObj.elements.L_4.checked  && formObj.elements.L_5.checked &&   !formObj.elements.L_6.checked && !formObj.elements.L_7.checked && !formObj.elements.L_8.checked){
	
	
			document.getElementById("a_Lr").style.display = "block";
			document.getElementById("a_Lr").style.backgroundColor = "#FADD8F";
			document.getElementById("a_Lr").style.fontSize = "12pt";
	}else if(formObj.elements.L_0.checked || formObj.elements.L_1.checked || formObj.elements.L_2.checked ||  formObj.elements.L_3.checked  ||  formObj.elements.L_4.checked  || formObj.elements.L_5.checked){
		document.getElementById("a_Lr1").style.display = "block";
			document.getElementById("a_Lr1").style.backgroundColor = "#FADD8F";
			document.getElementById("a_Lr1").style.fontSize = "12pt";
		}else {
			document.getElementById("a_Lw").style.display = "block";
			document.getElementById("a_Lw").style.backgroundColor = "#FADD8F";
			document.getElementById("a_Lw").style.fontSize = "12pt";
		}
	}else if (formname == 'L5_q1'){
		if ( formObj.elements.L_1.checked && formObj.elements.L_2.checked && formObj.elements.L_3.checked  && !formObj.elements.L_0.checked && !formObj.elements.L_4.checked){
		document.getElementById("a_Lr").style.display = "block";
			document.getElementById("a_Lr").style.backgroundColor = "#FADD8F";
			document.getElementById("a_Lr").style.fontSize = "12pt"
	}else if(formObj.elements.L_1.checked || formObj.elements.L_2.checked ||  formObj.elements.L_3.checked ){
		document.getElementById("a_Lr1").style.display = "block";
			document.getElementById("a_Lr1").style.backgroundColor = "#FADD8F";
			document.getElementById("a_Lr1").style.fontSize = "12pt";
	}else {
		document.getElementById("a_Lw").style.display = "block";
			document.getElementById("a_Lw").style.backgroundColor = "#FADD8F";
			document.getElementById("a_Lw").style.fontSize = "12pt";
	}

		
		
	}
	document.getElementById("check").disabled = true; 
	document.getElementById("check").setAttribute("disabled", "disabled");
	document.getElementById("check").style.backgroundColor = "#ebebeb";
	for (var h=0 ; h<elementlength ;h++){
		document.getElementById("L_"+h).setAttribute("disabled", "disabled");
	}
	
	
	
	
	
}
function validateFormChecks(formname) {
    var formObj = window.document.forms[formname];
    var elementlength=formObj.elements.length;
    var val  ="";
	correctanswer=-1;
	var j  =0;
    for( i=0;  i  < elementlength ; i++ ) {
		if(formObj.elements[i].type=="checkbox" ){
			if (formObj.elements[i].checked){
				document.getElementById("L_row"+i).style.backgroundColor = "#C4F371";
				j++;
			}else{
				document.getElementById("L_row"+i).style.backgroundColor = "#F39171";
			}		
        }
    }
	if (formname == 'L1_q1'){
		correctanswer=13;
	}else if (formname == 'L2_q4'){
		correctanswer=6;
	}	

	if (j==correctanswer){
		document.getElementById("a_Lr").style.display = "block";
		document.getElementById("a_Lr").style.backgroundColor = "#FADD8F";
		document.getElementById("a_Lr").style.fontSize = "12pt";
	
	}else{
		document.getElementById("a_Lw").style.display = "block";
		document.getElementById("a_Lw").style.backgroundColor = "#FADD8F";
		document.getElementById("a_Lw").style.fontSize = "12pt";
	
		
	}
	document.getElementById("check").disabled = true; 
	document.getElementById("check").setAttribute("disabled", "disabled");
	document.getElementById("check").style.backgroundColor = "#ebebeb";
	for (var h=0 ; h<elementlength ;h++){
		document.getElementById("L_"+h).setAttribute("disabled", "disabled");
	}

}




function validateFormL1Q8() {
    var formObj = window.document.forms.L1_q8;
    var elementlength=formObj.elements.length;
    var val  ="";
	var j  =0;
    for( i=0;  i  < elementlength ; i++ ) {
		
		if(formObj.elements[i].id=='L1_8_'+i){
			
			if (formObj.elements[i].value=='1'){
				j++;
				document.getElementById("L1_8_"+i).style.backgroundColor = "#C4F371";
			}else{
				document.getElementById("L1_8_"+i).style.backgroundColor = "#F39171";
			}
		}
    }
	var res_text="";
	if (j==4){
		res_text="Yes, your answers are correct! You have identified the relevant NROs and reporting methods for these events.";
	}else{
		res_text="Your answer is partially correct.";
	}
	document.getElementById("a_L1_8").style.backgroundColor = "#FADD8F";
	document.getElementById("a_L1_8").style.fontSize = "12pt";
	document.getElementById("a_L1_8").innerHTML=res_text;
	document.getElementById("check").disabled = true; 
	document.getElementById("check").setAttribute("disabled", "disabled");
	document.getElementById("check").style.backgroundColor = "#ebebeb";
	for (var h=0 ; h<=3;h++){
		document.getElementById("L1_8_"+h).setAttribute("disabled", "disabled");
	}
	

}

function validateFormL3Q3() {
    var formObj = window.document.forms.L3_q3;
    var elementlength=formObj.elements.length;
    var val  ="";
    var j=0;

	var element1=document.getElementById("L3_3_0");
	var element2=document.getElementById("L3_3_1");
	var element3=document.getElementById("L3_3_2");
	var element4=document.getElementById("L3_3_3");
	var element5=document.getElementById("L3_3_4");
	var element6=document.getElementById("L3_3_5");
	if(element1.value=='1'){
		j++;
		document.getElementById("L3_3_0").style.backgroundColor = "#C4F371";
	}else{
		document.getElementById("L3_3_0").style.backgroundColor = "#F39171";
	}
	if(element2.value=='1'){
		j++;
		document.getElementById("L3_3_1").style.backgroundColor = "#C4F371";
	}else{
		document.getElementById("L3_3_1").style.backgroundColor = "#F39171";
	}
if(element3.value=='1'){
		j++;
		document.getElementById("L3_3_2").style.backgroundColor = "#C4F371";
	}else{
		document.getElementById("L3_3_2").style.backgroundColor = "#F39171";
	}
if(element4.value=='1'){
		j++;
		document.getElementById("L3_3_3").style.backgroundColor = "#C4F371";
	}else{
		document.getElementById("L3_3_3").style.backgroundColor = "#F39171";
	}	
    if(element5.value=='0'){
		j++;
		document.getElementById("L3_3_4").style.backgroundColor = "#C4F371";
	}else{
		document.getElementById("L3_3_4").style.backgroundColor = "#F39171";
	}	
	    if(element6.value=='0'){
		j++;
		document.getElementById("L3_3_5").style.backgroundColor = "#C4F371";
	}else{
		document.getElementById("L3_3_5").style.backgroundColor = "#F39171";
	}	
	
	var res_text="";
	
	if (j==4){
		res_text="Yes, your answers are correct! Four of these events should lead to pest reporting. You could either create a new pest report on the International Phytosanitary Portal, or update an older report that already exists in relation to that pest and its outbreak.";
	}else{
		res_text="Your answer is partially correct.";
	}
	document.getElementById("a_L3_3").style.backgroundColor = "#FADD8F";
	document.getElementById("a_L3_3").style.fontSize = "12pt";
	document.getElementById("a_L3_3").innerHTML=res_text;
	document.getElementById("check").disabled = true; 
	document.getElementById("check").setAttribute("disabled", "disabled");
	document.getElementById("check").style.backgroundColor = "#ebebeb";
	for (var h=0 ; h<=3;h++){
		document.getElementById("a_L3_"+h).setAttribute("disabled", "disabled");
	}
	

}
function hasClass(element,cls) {
    var elements = element.getElementsByClassName(cls);
    return elements.length !== 0;
}



function doOnLoad() {
    if (hasClass(document.body, 'gapfilltable')) {
        someFunciton();
        var formulation = document.getElementsByClassName('formulation')[0];
        insertDivs(formulation.getElementsByClassName('draggable'));
    }
    if (hasClass(document.body, 'answercontainer')) {
        styleSpans();
        insertDivs(document.getElementsByClassName('drag'));
        refreshAnswer();
        document.addEventListener('mousedown', refreshAnswer);
    }

    // Toggle advice div
    if(hasClass(document.body, 'advice')) {
        var toggle  = document.getElementById("adviceToggle");
        var content = document.getElementById("adviceContent");
        
        toggle.addEventListener("click", function(e){
            e.preventDefault();
          content.style.display = (content.dataset.toggled ^= 1) ? "block" : "none";
        }, false);

    }

    if(hasClass(document.body, 'advice2')) {

        var toggle2  = document.getElementById("adviceToggle2");
        var content2 = document.getElementById("adviceContent2");

        toggle2.addEventListener("click", function(e){
            e.preventDefault();
            content2.style.display = (content2.dataset.toggled ^= 1) ? "block" : "none";
        }, false);

    }
	  if(hasClass(document.body, 'advice3')) {

        var toggle3  = document.getElementById("adviceToggle3");
        var content3 = document.getElementById("adviceContent3");

        toggle3.addEventListener("click", function(e){
            e.preventDefault();
            content3.style.display = (content3.dataset.toggled ^= 1) ? "block" : "none";
        }, false);

    }

    // Acronym finder
    if(hasClass(document.body, 'acronym')) {
        
        var acronymLink  = document.getElementById("acronymLink");
        var acronymContent = document.getElementById("acronymContent");
        var acronymClose = document.getElementById("acronymClose");

        acronymLink.addEventListener("click", function(e){
            e.preventDefault();
            acronymContent.style.display = (acronymContent.dataset.toggled ^= 1) ? "block" : "none";
        }, false);
        
        acronymClose.addEventListener("click", function(e){
           e.preventDefault();
           acronymContent.style.display = (acronymContent.dataset.toggled ^= 1) ? "block" : "none";  
        });
    } 
	
	 // res finder
    if(hasClass(document.body, 'resour')) {
        
        var resourLink  = document.getElementById("resourLink");
        var resourContent = document.getElementById("resourContent");
        var resourClose = document.getElementById("resourClose");
		
        resourLink.addEventListener("click", function(e){
            e.preventDefault();
            resourContent.style.display = (resourContent.dataset.toggled ^= 1) ? "block" : "none";
        }, false);
        
        resourClose.addEventListener("click", function(e){
           e.preventDefault();
           resourContent.style.display = (resourContent.dataset.toggled ^= 1) ? "block" : "none";  
        });
    }
 // res finder
    if(hasClass(document.body, 'helpclose')) {
        var helpClose1 = document.getElementById("helpclose1");
		helpClose1.addEventListener("click", function(e){
           e.preventDefault();
		   for (var i=1;i<6;i++){
		    var helpContent = document.getElementById("help"+i);
						helpContent.style.display =  "none";  
			}
        });
		var helpClose2 = document.getElementById("helpclose2");
		helpClose2.addEventListener("click", function(e){
           e.preventDefault();
		   for (var i=1;i<6;i++){
		    var helpContent = document.getElementById("help"+i);
						helpContent.style.display =  "none";  
			}
        });
		var helpClose3 = document.getElementById("helpclose3");
		helpClose3.addEventListener("click", function(e){
           e.preventDefault();
		   for (var i=1;i<6;i++){
		    var helpContent = document.getElementById("help"+i);
						helpContent.style.display =  "none";  
			}
        });
		var helpClose4 = document.getElementById("helpclose4");
		helpClose4.addEventListener("click", function(e){
           e.preventDefault();
		   for (var i=1;i<6;i++){
		    var helpContent = document.getElementById("help"+i);
						helpContent.style.display =  "none";  
			}
        });
		var helpClose5 = document.getElementById("helpclose5");
		helpClose5.addEventListener("click", function(e){
           e.preventDefault();
		   for (var i=1;i<6;i++){
		    var helpContent = document.getElementById("help"+i);
						helpContent.style.display =  "none";  
			}
        });
    }

}
var answers;
var count = 1;

// function nextAnswer() {
//     if (count > 0) {
//         answers[count - 1].style.display = "none";
//     }
//     answers[count].style.display = "block";
//     answers[count].style.width = "200px";
//     count++;
// }

function someFunciton() {
    //document.addEventListener('dblclick', nextAnswer);

    var gapquestion = document.getElementsByClassName('gapquestion')[0];
    var inputs = gapquestion.getElementsByTagName('input');
    for (var j = 0; j < inputs.length; j++) {
        var input = inputs[j];
        input.style.width = "99%";
    }

    var formulation = document.getElementsByClassName('formulation')[0];
    answers = formulation.getElementsByClassName('draggable');
    for (var i = 0; i < answers.length; i++) {
        var answer = answers[i];
        answer.style.width = "200px";
        answer.style.display = "none";
        answer.style.overflow = 'hidden';
    }
    answers[0].style.display = "block";
}

function refreshAnswer() {
    var spansDiv1 = document.getElementsByClassName('answercontainer');
    var spans1 = spansDiv1[0].getElementsByTagName('span');

    for (var i = 0; i < spans1.length; i++) {
        spans1[i].style.display = "none";
    }
    var spansDiv2 = document.getElementsByClassName('drags');
    var spans2 = spansDiv2[0].getElementsByTagName('span');

    for (var j = 0; j < spans2.length; j++) {
        if (spans2[j].classList.contains('unplaced')) {
            var span = spans1[j];
            addDivFor(span);
            span.style.display = "inline";
            span.addEventListener('drop', refreshAnswer);
            console.log('added dragend');
            break;
        }
    }
}

function styleSpans() {
    this.styleThese = function (elements) {
        for (var i = 0; i < elements.length; i++) {
            var span = elements[i];
            span.style.width = '200px';
            span.style.overflow = 'hidden';
        }
    };

    var spans1 = document.getElementsByClassName('drags')[0].getElementsByTagName('span');
    this.styleThese(spans1);

    var spans2 = document.getElementsByClassName('drop');
    this.styleThese(spans2);
}

function insertDivs(dragSpans) {

    for (var j = 0; j < dragSpans.length; j++) {

        var div = addDivFor(dragSpans[j]);

        var mouseOver = function(div) {
            return function (event) {
                var span = event.target;
                var rect = span.getBoundingClientRect();
                div.style.top = (rect.top + 30 + window.scrollY) + 'px';
                div.style.left = rect.left + 'px';
                div.style.display = "inline";
            };
        }(div);

        var mouseOut = function(div) {
            return function () {
                div.style.display = "none";
            };
        }(div);

        dragSpans[j].addEventListener('mouseover', mouseOver, false);

        dragSpans[j].addEventListener('mouseout', mouseOut, false);
    }
}

function addDivFor(span) {
    var div = document.createElement("textarea");
    div.style.color = "#5b2283";
    div.innerHTML = span.innerHTML;
    var size = div.innerHTML;
    div.style.height = (Math.ceil(size.length / 20)*10) + "px";
    div.style.width = "400px";
    div.style.padding = "10px";
    div.style.fontSize = "15px";
    div.style.position = 'absolute';
    div.style.top = "0";
    div.style.display = "none";
    div.style.zIndex = "100";

    document.body.appendChild(div);

    return div;
}

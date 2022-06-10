$(function () {
	$("#searchInput").autocomplete({
		source: List,
		focus : function(event, ui) {	
			return false;
		},
		minLength: 1,
		delay: 100,
	});
});
List=['간장', '계란', '고추장', '과자', '기저귀', '껌', '냉동만두', '된장', '두루마리화장지', '두부', '라면', '마요네즈', '맛김', '맛살', '맥주', '밀가루', '분유', '사이다', '생리대', '생수', '샴푸', '설탕', '세탁세제', '소주', '시리얼', '식용유', '쌈장', '아이스크림', '어묵', '오렌지주스', '우유', '즉석밥', '참기름', '참치 캔', '커피', '케첩', '콜라', '햄']
//id, class, tagname 선택시에 querySelector보다 getElementById, getElementsByClassName, getElementsByTagName 사용이 빠르다
/*
window.onload = function(){
	const buttons = document.querySelectorAll(".btn")
	for (let button of buttons) {
		button.addEventListener('click', function(){
			
			let result = confirm("장바구니 페이지로 이동하시겠습니까?");
			if(result){
				//location.href = "basket";
				//location.href = "basket";
				//frm.submit();
				return true;
			}else{
				return false;
			}
			
			//frm.submit();
		})
	}		
}
*/

//document.querySelectorAll(".btn").addEventListener("click", function(){
/*
document.querySelector(".btn").addEventListener("click", function(){
	let btn = document.querySelectorAll(".btn");
	for (let i=0; i<btn.length; i++){
		btn[i]
	}
	
	let result = confirm("장바구니 페이지로 이동하시겠습니까?");
	if(result){
		location.href = "basket";
	}else{
		return false;
	}
})	
*/

//document.querySelector(".btn").addEventListener("click", function(){
//document.querySelectorAll(".btn").addEventListener("click", function(){
//	console.log("1");	
//})

//const sections = document.querySelectorAll("#tb , #tb .btn");
//console.log(sections.constructor.name);

//body > div > div.row.items > div > table > tbody > tr:nth-child(1) > td:nth-child(8) > button
//body > div > div.row.items > div > table > tbody > tr:nth-child(2) > td:nth-child(8) > button
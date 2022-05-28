/**
 * 
 */
 /*
let items = false;
	
function update_selected() {
  $("#itemSelect").val(0);
  $("#itemSelect").find("option[value!=0]").detach();

  $("#itemSelect").append(items.filter(".item_" + $(this).val()));
}

$(function() {
  items = $("#itemSelect").find("option[value!=0]");
  items.detach();

  $("#productSelect").change(update_selected);
  $("#productSelect").trigger("change");
});
*/
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

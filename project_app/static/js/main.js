/**
 * 
 */
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
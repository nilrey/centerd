var arrTabs = [];
var arrMenus = [];

function manageSubmenu(line, pnt){
	if($('#'+line).css('display') == 'none'){
		$('.sub-menu').hide();
		$('.menu-plate').removeClass("plate-sel");
	    $(pnt).toggleClass("plate-sel");
	    $('#'+line).show(200);
	}else{
		$('.menu-plate').removeClass("plate-sel");
	    $('#'+line).hide(200);
	}
}

function setTabsActive() {
    if ( arrTabs.length > 0 ) {
        for( i in arrTabs ){  
            $("#"+arrTabs[i]).addClass("active");
        }
    }
}

function setLeftMenuActive() {
    if ( arrMenus.length > 0 ) {
        for( i in arrMenus ){  
            $("#"+arrMenus[i]).removeClass("displayNone");
        }
    }
}

function getModalDialogInfo(msg, error = '0'){ 
  if(error == '1' ) {
    $('#dialogModalLabel').html('Ошибка');
    $('#dialogModalHeader').css('background-color', 'red' );
  }
  var modal = new bootstrap.Modal(document.getElementById('dialog-modal-info'), {});
  $('#dialog-msg-info').html(msg);
  modal.show();
}


function getModalDialogConfirm(msg){
  var modal = new bootstrap.Modal(document.getElementById('dialog-modal-confirm'), {});
  $('#dialog-msg-confirm').html(msg);
  modal.show();
}

function getModalDialogForm(msg, header){
  var modal = new bootstrap.Modal(document.getElementById('dialog-modal-form'), {});
  $('#dialog-msg-form').html(msg);
  $('#formModalLabel').html(header);

  modal.show();
}

function confirmDelete(recordTitle, deleteUrl){
    getModalDialogConfirm('Вы действительно хотите удалить запись "'+recordTitle+'"?');
    $('#dialog-modal-confirm-send').click( function() {window.location.replace(deleteUrl)} );
}

$(document).ready( function (){
	setLeftMenuActive();
    setTabsActive();
} )
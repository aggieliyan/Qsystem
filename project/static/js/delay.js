function refuse_delay(id){
				$('#delayid').val(id);
				$('#myModal').modal('show');
			}
			
			function do_refuse(){
				$('#test_form').submit();
			}
			
			function approve_delay(id){
				$('#delayid1').val(id);
				$('#myModal_approve').modal('show');
			}
			
			function do_approve(){
				
				$('#approve_form').submit();
			}
function toggleFold(fold_id) {
	if ($("div#fold_" + fold_id).is(":visible")) {
		$("span.fold_on_id_" + fold_id).hide()
		$("span.fold_off_id_" + fold_id).show()
	} else {
		$("span.fold_on_id_" + fold_id).show()
                $("span.fold_off_id_" + fold_id).hide()
	}

	$("div#fold_" + fold_id).toggle()
}

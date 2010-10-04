jQuery.fn.dataTableExt.oSort['currency-asc'] = function(a,b) {
	/* Remove any commas (assumes that if present all strings will have a fixed number of d.p) */
	var x = a == "-" ? 0 : a.replace( /,/g, "" );
	var y = b == "-" ? 0 : b.replace( /,/g, "" );
	
	/* Remove the currency sign */
	x = x.substring( 1 );
	y = y.substring( 1 );
	
	/* Parse and return */
	x = parseFloat( x );
	y = parseFloat( y );
	return x - y;
};
jQuery.fn.dataTableExt.oSort['currency-desc'] = function(a,b) {
	/* Remove any commas (assumes that if present all strings will have a fixed number of d.p) */
	var x = a == "-" ? 0 : a.replace( /,/g, "" );
	var y = b == "-" ? 0 : b.replace( /,/g, "" );
	
	/* Remove the currency sign */
	x = x.substring( 1 );
	y = y.substring( 1 );
	
	/* Parse and return */
	x = parseFloat( x );
	y = parseFloat( y );
	return y - x;
};
jQuery.fn.dataTableExt.oSort['formatted-num-asc'] = function(x,y){
    x = x.replace(/[^\d\-\.\/]/g,'');
    y = y.replace(/[^\d\-\.\/]/g,'');
    if(x.indexOf('/')>=0)x = eval(x);
    if(y.indexOf('/')>=0)y = eval(y);
    return x/1 - y/1;
}
jQuery.fn.dataTableExt.oSort['formatted-num-desc'] = function(x,y){
    x = x.replace(/[^\d\-\.\/]/g,'');
    y = y.replace(/[^\d\-\.\/]/g,'');
    if(x.indexOf('/')>=0)x = eval(x);
    if(y.indexOf('/')>=0)y = eval(y);
    return y/1 - x/1;
}
jQuery.fn.dataTableExt.oSort['title-string-asc']  = function(a,b) {
	var x = a.match(/title="(.*?)"/)[1].toLowerCase();
	var y = b.match(/title="(.*?)"/)[1].toLowerCase();
	return ((x < y) ? -1 : ((x > y) ?  1 : 0));
};

jQuery.fn.dataTableExt.oSort['title-string-desc'] = function(a,b) {
	var x = a.match(/title="(.*?)"/)[1].toLowerCase();
	var y = b.match(/title="(.*?)"/)[1].toLowerCase();
	return ((x < y) ?  1 : ((x > y) ? -1 : 0));
};

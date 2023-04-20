num : SIGNED_NUMBER ;

SIGNED_NUMBER: [-]?[0-9]+([.]([0-9]*)?)? | [-]?[.][0-9]+ ;

WHITESPACE : ' ' -> skip ;


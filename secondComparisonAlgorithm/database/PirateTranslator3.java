public class PirateTranslator {

    String[] phrases = {"hello", "hi", "is", "pardon me", "excuse me",
			"my", "friend", "sir", "madam",
			"stranger", "officer",
			"where", "you", "tell",
			"know", "how far", "old", "happy"};
    String[] piratetalk = {"ahoy", "yo-ho-ho", "be", "avast", "arrr",
			   "me", "me bucko", "matey", "proud beauty",
			   "scurvy dog", "foul blaggart",
			   "whar", "ye", "be tellin'",
			   "be knowin'", "how many leagues",
			   "barnacle-covered", "grog-filled"};
	
    String[] positiveWords = {"adore", "enjoy", "love"};
    String[] negativeWords = {"hate", "despise", "dislike"};
    
    String[] lastTranslations = new String[25];
    int s = 0;

    /**
    * _Part 1: Implement this method_
    *
    * Translate the input string and return the resulting string
    */ 
    public String translate(String input) {
	String pirate = input.toLowerCase();
	for (int i = 0; i < phrases.length; i++) {
	    pirate = pirate.replace(phrases[i], piratetalk[i]);
	}


	int affect = 0;
	for(int i = 0; i < positiveWords.length; i++) {
	    if (pirate.contains(positiveWords[i])) {
		affect = 1;
		break;
	    }
	}
	for(int i = 0; i < negativeWords.length; i++) {
	    if (pirate.contains(negativeWords[i])) {
		affect -= 1; // making it either 0 or -1
		break;
	    }
	}
	String suffix = "";
	if (affect == 1) suffix = " 'tis like me pirate treasure!";
	if (affect == -1) suffix =  " 'tis like bein' food for the fish!";

	pirate = pirate + suffix;

	// remove multiple "me"...
	
	return pirate;
	
    }

    
    //   begin solution...
    //   this is extra credit, and shouldn't appear in the stub.
    public String translateWithCase(String input) {
	StringBuffer sb = new StringBuffer(input.length()*2);

	char control = '_';
	String uppercase = input.toUpperCase();
	
	for(int i = 0; i < input.length(); i++) {
	    if (input.charAt(i) == uppercase.charAt(i)) {
		sb.append(control);
	    }
	    sb.append(input.charAt(i));
	}
	String lpirate = translate(sb.toString());
	sb = new StringBuffer(20);
	boolean makeUpper = false;
	for(int i = 0; i < lpirate.length(); i++) {
	    
	    if (lpirate.charAt(i) == control) {
		makeUpper = true;
	    } else {
		if (makeUpper) {
		    String u = "" + lpirate.charAt(i);
		    sb.append(u.toUpperCase());
		    makeUpper = false;
		} else {
		    sb.append(lpirate.charAt(i));
		}
	    }
	}

	return sb.toString();
    }
    // end solution 
}

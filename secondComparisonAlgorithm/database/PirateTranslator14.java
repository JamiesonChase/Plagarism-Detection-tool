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
    	input=input.toLowerCase();
		for (int i=0; i<phrases.length; i++) {
			if (input.contains(phrases[i])) {
				if (input.length()==phrases[i].length() || input.contains(" "+phrases[i]+" ") || input.contains(" "+phrases[i])
					|| input.contains(phrases[i]+" ")) input=(input.replace(phrases[i], piratetalk[i]));
			}
		}
		for (int i=0; i<3; i++) {
			if (input.contains(positiveWords[i])) input=input+" 'tis like me pirate treasure!";
			if (input.contains(negativeWords[i])) input=input+" 'tis like bein' food for the fish!";
		}
			return input;
    }


    
}

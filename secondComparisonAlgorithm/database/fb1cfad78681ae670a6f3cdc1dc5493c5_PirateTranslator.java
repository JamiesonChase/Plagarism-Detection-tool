public class PirateTranslator {

    String[] phrases = {"hello", "hi", "is", "pardon me", "excuse me",
			"my", "friend", "sir", "madam",
			"stranger", "officer",
			"where", "you", "tell",
			"know", "how far", "old", "happy"};
    
    String[] positive = {"adore","love","enjoy"};
    
    String[] negative = {"dislike","hate","despise"};
    
    String[] piratetalk = {"ahoy", "yo-ho-ho", "be", "avast", "arrr",
			   "me", "me bucko", "matey", "proud beauty",
			   "scurvy dog", "foul blaggart",
			   "whar", "ye", "be tellin'",
			   "be knowin'", "how many leagues",
			   "barnacle-covered", "grog-filled"};
	
    String[] positiveWords = {"adore", "enjoy", "love", " 'tis like me pirate treasure!"};
    String[] negativeWords = {"hate", "despise", "dislike", " 'tis like bein' food for the fish!"};
    
    String[] lastTranslations = new String[25];
    int s = 0;

    /**
    * _Part 1: Implement this method_
    *
    * Translate the input string and return the resulting string
    */ 
    public String translate(String input) {
    	
    	input = input.toLowerCase();
    	

		for (int i = 0; i < (phrases.length); i++) {
			input = (input.replace(phrases[i], piratetalk[i]));
			}
		
    	for (int k = 0; k < 4; k++) {
			if (input.contains(positiveWords[k])) {
				input += positiveWords[3];
				break;
			}
			if (input.contains(negativeWords[k])) {
				input += negativeWords[3];
				break;
			}
			
		}
		input = (input.replace("despbee", "despise"));
		return input;
	 }
  
}

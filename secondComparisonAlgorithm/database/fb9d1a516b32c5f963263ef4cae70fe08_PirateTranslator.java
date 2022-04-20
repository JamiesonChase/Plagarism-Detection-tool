public class PirateTranslator {

//  below are the English phrases (phrases) and corresponding Pirate phrases (piratetalk)
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
//	below are words to help determine whether the affect of the input is positive or negative
    String[] positiveWords = {"adore", "enjoy", "love"};
    String[] negativeWords = {"hate", "despise", "dislike"};
    
    String[] lastTranslations = new String[25];
    int s = 0;

     /**
     * translate() is a method that takes as input a string (in English) and outputs that string
     * translated into Pirate-speech. It also detects the affect of the input phrase and appropriately
     * appends a Pirate metaphor onto the end of the string. If there is both a positive and negative
	 * affect in the sentence, nothing will be appended.
     */
    public String translate(String input) {
    	int positive = 0;
    	int negative = 0;
    	input=input.toLowerCase();
// 		this for loop replaces English phrases with corresponding Pirate phrases
		for (int i=0; i<phrases.length; i++) {
			if (input.contains(phrases[i])) {
				if (input.length()==phrases[i].length() || input.contains(" "+phrases[i]+" ") || input.contains(" "+phrases[i])
					|| input.contains(phrases[i]+" ")) input=(input.replace(phrases[i], piratetalk[i]));
			}
		}
//		this for loop detects the affect of the sentence and appends the appropriate metaphor
		for (int i=0; i<3; i++) {
			if (input.contains(positiveWords[i])) positive++;
			if (input.contains(negativeWords[i])) negative++;
			}
			if ((positive==0 && negative==0) || (positive!=0 && negative!=0)) input=input;
			else {
				if (positive>0) input=input+" 'tis like me pirate treasure!";
				if (negative>0) input=input+" 'tis like bein' food for the fish!";
		}
			return input;
    }
}

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
  private boolean isPositive(String input){
    for( String word : positiveWords){
      if(input.contains(word)) return true;
    }
    return false;
  }
  private boolean isNegative(String input){
    for( String word : negativeWords){
      if(input.contains(word)) return true;
    }
    return false;
  }
    /**
    * _Part 1: Implement this method_
    *
    * Translate the input string and return the resulting string
    */
    public String translate(String input) {
	// TODO: implement this
      input = input.toLowerCase();
      String result = "";

      for(int i=0; i<phrases.length; i++){
        if(input.contains(phrases[i])){
          input = input.replace(phrases[i],piratetalk[i] );
        }
      }
     if(isPositive(input) && !isNegative(input)){
       input += "'tis like me pirate treasure!";
     }else if(!isPositive(input) && isNegative(input)){
       input += "'tis like bein' food for the fish!";
     }

      return input;
    }


}
/**
 * Eric Stadelman and Charlie Broadbent
 * Paddle.java
 * A subclass used to  reset our paddle
 */

package breakout;

import javafx.scene.shape.Rectangle;

public class Paddle extends Rectangle {

    public Paddle(){
    }

    public void reset(){
        setLayoutX(100);
    }
}



package pong;


import javafx.fxml.FXML;
import javafx.scene.shape.Rectangle;
import javafx.scene.paint.Paint;
import javafx.scene.paint.Color;

public class Brick extends Rectangle {


    @FXML private double layoutX;
    @FXML private double layoutY;

    @FXML private double height;
    @FXML private double width;

    @FXML private String id;


    @FXML private String fill;
    private int hitsLeft;


    public Brick(double x, double y){
        this.setWidth(100);
        this.setHeight(25);
        this.hitsLeft = 0;
        this.setX(x*145 + 10);
        this.setY(y * 50 + 25);
        this.setFill((Color.color(Math.random(), Math.random(), Math.random())));
        this.setStroke(Color.BLACK);
        this.id = "brick" + x + y;


    }

    private void remove(){
        this.height = 0;
        this.width = 0;

    }

    public boolean isDestroyed(){
        if (this.hitsLeft<0) {
            return true;
        }
        else{
            return false;
        }

    }

    private int getHits(){
        return hitsLeft;
    }
    public void hit(){
        this.hitsLeft--;
        if (this.getHits() == 0){
            this.remove();
        }
    }

}


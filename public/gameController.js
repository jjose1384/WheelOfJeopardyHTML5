/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

// default game properties
var gameTimerDefault = 5; // in seconds
var spinsLeftDefault = 50;
var questionsLeftDefault = 30;

// fixed categories
var category_bankrupt = "Bankrupt";
var category_loseTurn = "Lose Turn";
var category_freeTurn = "Free Turn";
var category_spinAgain = "Spin Again";
var category_playerChoice = "Player's Choice";
var category_opponentChoice = "Opponent's Choice";

function GameController(wheelParam, boardParam, playerListParam, categoryListParam, roundNumberParam)
{
    this.wheel = wheelParam;
    this.board = boardParam;
    this.spinsLeft = spinsLeftDefault;
    this.questionsLeft = questionsLeftDefault;
    this.gameTimer = gameTimerDefault; // in seconds
    this.roundNumber = roundNumberParam; // 1 or 2
    this.currentPlayerIndex = 0; // index of the player whose turn it is
    this.playerList = playerListParam;
    this.timer; // used to start and stop timer

    // set defaultCategories
    categoryListParam[6].title = category_bankrupt;
    categoryListParam[7].title = category_loseTurn;
    categoryListParam[8].title = category_freeTurn;
    categoryListParam[9].title = category_spinAgain;
    categoryListParam[10].title = category_playerChoice;
    categoryListParam[11].title = category_opponentChoice; 

    this.board.setCategories(categoryListParam);
    
        
    this.shuffle(this.board.categoryTitleList);
    this.wheel.setLabels(this.board.categoryTitleList);
}

GameController.prototype = {
    startGame: function ()
    {
        this.setPlayerNames();
        this.updateSpinsLeft();
        this.updateCurrentPlayer();
        this.updateRoundNumber();
        this.updateSelectedCategory();
        this.updateSelectedQuestion();
        
        // update player score
        for (var i = 0; i < 3; i++)
        {
            this.updatePlayerScore(i);
        }
        
        this.enableSpinButton(0); // for player 0
        
        this.board.populateJeopardyBoard();
        this.wheel.draw(0, false);
    },
    
    startCountdownTimer: function ()
    {
        var self = this;
        self.gameTimer = gameTimerDefault;
        var outputId = "timer";
        self.timer = setInterval(function () 
        {
            // Display the result in the element with outputId
            document.getElementById(outputId).innerHTML = self.gameTimer;

            // If the count down is finished, write some text 
            if (self.gameTimer <= 0) 
            {
                self.resetTimer();
                
                // play timeup sound
                var audio = new Audio('sound/timeUp.mp3');
                audio.play();
                
                self.enableModeratorButtons(true);
            }

            self.gameTimer--;
        }, 1000);
    },
        
    // sets the player's names on the screen
    setPlayerNames: function()
    {
        var self = this;
        document.getElementById("player0Name").innerHTML = self.playerList[0].name;
        document.getElementById("player1Name").innerHTML = self.playerList[1].name;
        document.getElementById("player2Name").innerHTML = self.playerList[2].name;
    },
        
    // updates spins left on the screen
    updateSpinsLeft: function ()
    {
        var self = this;
        var outputId = "spinsLeft";
        document.getElementById(outputId).innerHTML = self.spinsLeft;
    },
        
    // updates Category title on the screen
    updateSelectedCategory: function()
    {
        var self = this;
        var outputId = "selectedCategory";
        if (self.board.selectedCategory !== null)
        {
            document.getElementById(outputId).textContent = self.board.selectedCategory.title; // display category
        }
        else 
        {
            document.getElementById(outputId).textContent = "";
        }
    },
    
    // updates Question on the screen
    updateSelectedQuestion: function()
    {
        var self = this;
        var outputId = "selectedQuestion";
        if (self.board.selectedCategory !== null)
        {
            document.getElementById(outputId).textContent = self.board.selectedCategory.selectedQuestion.questionText; // display question
        }
        else
        {
            document.getElementById(outputId).textContent = "";
        }
            
    },
    
    // updates Answer text on the screen
    updateAnswer: function()
    {
        var self = this;
        var outputId = "answer";
        if (self.board.selectedCategory !== null)
        {
            document.getElementById(outputId).textContent = self.board.selectedCategory.selectedQuestion.answerText; // display answer
        }
        else
        {
            document.getElementById(outputId).textContent = "";
        }
            
    },
        
    // update current player name on the screen based on name
    updateCurrentPlayer: function ()
    {
        var self = this;
        var outputId = "currentPlayerName";
        var popupHeader = "popupHeader";
        var currentPlayer = self.playerList[self.currentPlayerIndex];
        
        document.getElementById(outputId).innerHTML = currentPlayer.name;
        document.getElementById(popupHeader).innerHTML = currentPlayer.name;
    },
        
    // updates score for player on the screen
    updatePlayerScore: function(playerIndex) // playerIndex: 0-2 
    {
        var self = this;
        var outputId = "player" + playerIndex + "Score";
        var selectedPlayer = self.playerList[playerIndex];
        document.getElementById(outputId).innerHTML = selectedPlayer.getScore(self.roundNumber);
    },
       
    // updates tokens for player on the screen
    updatePlayerTokens: function(playerIndex) // playerIndex: 0-2 
    {
        var self = this;
        var selectedPlayer = self.playerList[playerIndex];
        
        var outputId = "player" + playerIndex + "Tokens";
        document.getElementById(outputId).innerHTML = selectedPlayer.tokens;
        
        // update popup token
        document.getElementById("popupTokens").innerHTML = selectedPlayer.tokens;
    },
        
    // updates Round Number
    updateRoundNumber: function()
    {
        var self = this;
        
        var outputId = "roundNumber";
        document.getElementById(outputId).innerHTML = self.roundNumber;
    },
    
    updateJeopardyBoard: function()
    {
        var self = this;
        
        var outputId = "valueC"+self.board.selectedCategoryIndex+"Q"+self.board.selectedCategory.selectedQuestionIndex;
        document.getElementById(outputId).innerHTML = ""
    },
        
    incrementPlayer: function()
    {
        var self = this;
        self.currentPlayerIndex++;
        if (self.currentPlayerIndex > 2)
        {
            self.currentPlayerIndex = 0;
        }
    },
        
    disableSpinButtons: function()
    {
        document.getElementById("player0Spin").disabled = true;
        document.getElementById("player1Spin").disabled = true;
        document.getElementById("player2Spin").disabled = true;
    },
        
    enableSpinButton: function(playerIndex) // options are: player0Spin|player1Spin|player2Spin
    {
        document.getElementById("player" + playerIndex + "Spin").disabled = false;
    },
    
    disableModeratorButtons: function()
    {
        document.getElementById("correctButton").disabled = true;
        document.getElementById("incorrectButton").disabled = true;
        document.getElementById("timeExpiredButton").disabled = true;
    },
    
    enableModeratorButtons: function(timeExpiredEnabled)
    {
        
        document.getElementById("correctButton").disabled = false;
        document.getElementById("incorrectButton").disabled = false;
        
        if (timeExpiredEnabled)
        {
            document.getElementById("timeExpiredButton").disabled = false;
        }
        else
        {
            document.getElementById("timeExpiredButton").disabled = true;
        }
    },
    
    /*
     * Shuffles a passed in array. Used to shuffle options on the wheel
     * 
     */
    shuffle: function (array) 
    {
        var currentIndex = array.length, temporaryValue, randomIndex;
        
        // While there remain elements to shuffle...
        while (0 !== currentIndex) 
        {

            // Pick a remaining element...
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex -= 1;
            // And swap it with the current element.
            temporaryValue = array[currentIndex];
            array[currentIndex] = array[randomIndex];
            array[randomIndex] = temporaryValue;
        }

        return array;
    },


    processWheelCategory: function(categoryText)
    {
        var self = this;

        // update spinsLeft and current Category for every case
        self.updateSpinsLeft();
        
        self.board.findCategoryByTitle(categoryText);
        self.updateSelectedCategory();

        if (categoryText === category_bankrupt)
        {
            // play bankrupt sound
            var audio = new Audio('sound/Wheel-of-fortune-bankrupt.mp3');
            audio.play();
            
            var currentPlayer = self.playerList[self.currentPlayerIndex];
            currentPlayer.setScore(0, self.roundNumber);
            
            self.updatePlayerScore(self.currentPlayerIndex);

            self.incrementPlayer();
            self.updateCurrentPlayer();
            
            self.enableSpinButton(self.currentPlayerIndex);
            
            // check for end of round
            if (self.spinsLeft <= 0 || self.questionsLeft <= 0)
            {
                // round has ended
                self.endOfRound();
            }
        } 
        else if (categoryText === category_loseTurn)
        {
            // option to use token
            var currentPlayer = self.playerList[self.currentPlayerIndex];
            if (currentPlayer.tokens > 0)
            {
                self.useTokenModalPopup()();
            }
            else // normal flow for lose turn
            {
                self.loseTurnFlow();
            }
            
            // check for end of round
            if (self.spinsLeft <= 0 || self.questionsLeft <= 0)
            {
                // round has ended
                self.endOfRound();
            }
        } 
        else if (categoryText === category_freeTurn)
        {
            var currentPlayer = self.playerList[self.currentPlayerIndex];
            currentPlayer.tokens++;
            self.updatePlayerTokens(self.currentPlayerIndex);

            self.enableSpinButton(self.currentPlayerIndex);
                        
            // check for end of round
            if (self.spinsLeft <= 0 || self.questionsLeft <= 0)
            {
                // round has ended
                self.endOfRound();
            }
        } 
        else if (categoryText === category_spinAgain)
        {
            self.enableSpinButton(self.currentPlayerIndex);
                        
            // check for end of round
            if (self.spinsLeft <= 0 || self.questionsLeft <= 0)
            {
                // round has ended
                self.endOfRound();
            }
        } 
        else if (categoryText === category_playerChoice)
        {
            self.board.enableCategoryButtons();
        } 
        else if (categoryText === category_opponentChoice)
        {
            self.board.enableCategoryButtons();
        } 
        else // one of the jeopardy categories selected
        {
            if (self.board.selectedCategory.isCategoryAvailable())
            {
                self.updateSelectedQuestion();
                self.updateJeopardyBoard(); // clear out value
                self.questionsLeft--; // decrement questions
            
                self.enableModeratorButtons(false);
                self.startCountdownTimer();
            }
            else 
            {
                // Spin again
                self.enableSpinButton(self.currentPlayerIndex);          
            }
        }
    },
    
    spinWheel: function()
    {
        var self = this;
        
        self.spinsLeft--;
        self.disableSpinButtons();
        self.wheel.spin(self);
        
        /* clear selected category
         * clear selected question
         * clear answer
         */
        
        self.board.selectedCategory = null;
        self.board.selectedCategoryIndex = null;
        self.updateSelectedCategory();
        self.updateSelectedQuestion();
        self.updateAnswer();
        
    },
    
    selectCategory: function(selectedCategoryIndexParam)
    {
        var self = this;
        
        self.board.disableCategoryButtons();
        
        self.board.selectedCategoryIndex = selectedCategoryIndexParam;
        self.board.selectedCategory = self.board.categoryList[selectedCategoryIndexParam];
        self.updateSelectedCategory();
        
        self.updateSelectedQuestion();
        self.updateJeopardyBoard(); // clear out value

        self.enableModeratorButtons();
        self.startCountdownTimer();
        
    },
    
    useTokenModalPopup: function()
    {
        var self = this; 
        self.updateCurrentPlayer();
        self.updatePlayerTokens(self.currentPlayerIndex);
        
        $("#useTokenModal").modal({backdrop: "static"});
    },
  
    messageModalPopup: function(message, startRound2)
    {   
        document.getElementById("gameMessage").innerHTML = message;
        
        if (startRound2 === true)
        {
            document.getElementById("startRound2").style.display = "block";
            document.getElementById("ok").style.display = "none";
        }
        else
        {
            document.getElementById("startRound2").style.display = "none";
            document.getElementById("ok").style.display = "block";
        }
        
        $("#messageModal").modal({backdrop: "static"});
    },
    
    // end of round or game
    endOfRound: function()
    {
        var self = this;
        
        if (self.roundNumber === 1)
        {
            self.messageModalPopup("Round has ended, lets start the next round!", true);
        }
        else // game has ended
        {
            self.messageModalPopup("Game has ended! <br/> Congratulations!", false);
        }
    },
    
    loseTurnFlow: function()
    {
        var self = this;
        
        self.incrementPlayer();
        self.updateCurrentPlayer();
        self.enableSpinButton(self.currentPlayerIndex);
    },
    
    useTokenFlow: function()
    {
        var self = this;
        var currentPlayer = self.playerList[self.currentPlayerIndex];
        currentPlayer.tokens--; 
        self.updatePlayerTokens(self.currentPlayerIndex);
        
        self.enableSpinButton(self.currentPlayerIndex);
    },
    
    selectCorrect: function()
    {
        var self = this;
        
        self.disableModeratorButtons();
        self.resetTimer();
        
        var currentPlayer = self.playerList[self.currentPlayerIndex];
        currentPlayer.addSubtractScore(self.board.selectedCategory.selectedQuestion.value,
                                       self.roundNumber); // add the value to the player's score        
        self.updatePlayerScore(self.currentPlayerIndex);

        
        self.board.selectedCategory.incrementSelectedQuestion();
        self.enableSpinButton(self.currentPlayerIndex);
        
        // check for end of round
        if (self.spinsLeft <= 0 || self.questionsLeft <= 0)
        {
            // round has ended
            self.endOfRound();
        }
    },
    
    selectIncorrect: function()
    {
        var self = this;
        
        self.disableModeratorButtons();
        self.resetTimer();
        
        var currentPlayer = self.playerList[self.currentPlayerIndex];
        currentPlayer.addSubtractScore(0 - self.board.selectedCategory.selectedQuestion.value, 
                                       self.roundNumber); // subtract the value from the player's score 
        self.updatePlayerScore(self.currentPlayerIndex);
        
        self.board.selectedCategory.incrementSelectedQuestion();
        
        // check for end of round
        if (self.spinsLeft <= 0 || self.questionsLeft <= 0)
        {
            // round has ended
            self.endOfRound();
        }
        else // only show free spin token popup if the round hasn't ended
        {
            if (currentPlayer.tokens > 0)
            {
                self.useTokenModalPopup();
            }
            else // normal flow for lose turn
            {
                self.loseTurnFlow();
            }
        }
    },
    
    selectTimeExpired: function()
    {
        var self = this;
        
        self.disableModeratorButtons();
        self.resetTimer();
        
        var currentPlayer = self.playerList[self.currentPlayerIndex];
        
        self.board.selectedCategory.incrementSelectedQuestion();
        
        // check for end of round
        if (self.spinsLeft <= 0 || self.questionsLeft <= 0)
        {
            // round has ended
            self.endOfRound();
        }
        else // only show free spin token popup if the round hasn't ended
        {
            if (currentPlayer.tokens > 0)
            {
                self.useTokenModalPopup();
            }
            else // normal flow for lose turn
            {
                self.loseTurnFlow();
            }
        }
    },
    
    // stops the timer and resets timer back to 0
    resetTimer: function()
    {
        var self = this;
        var outputId = "timer"
        
        clearInterval(self.timer); // stop timer
        document.getElementById(outputId).innerHTML = "0";
    }
};


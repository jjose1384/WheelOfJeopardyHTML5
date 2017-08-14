/*
 * The board object is used to keep track of the Jeopardy board
 * and all related functions
 */
function Board() {
    this.selectedCategoryIndex = null; // index of categories 0-5
    this.selectedCategory = null;
    this.categoryList = [];
    this.categoryTitleList = [];
}

Board.prototype = {
    setCategories: function(categoryListParam)
    {
        var self = this;
        
        self.categoryList = categoryListParam; // list of category objects
        
        self.categoryTitleList = []; // list of category titles
        self.getCategoryTitles(); // set Category titles
    },
    
    // sets and returns the category based on the categoryTitle;
    findCategoryByTitle: function(categoryTitleParam)
    {
        
        var self = this;
        for (var i = 0; i < self.categoryList.length; i++)
        {
            if (self.categoryList[i].title === categoryTitleParam)
            {
                self.selectedCategory = self.categoryList[i];
                self.selectedCategoryIndex = i;
                return self.categoryList[i];
            }
        }
    },
    
    // load the values
    populateJeopardyBoard: function()
    {
        var self = this;
        // populate category titles
        for (var k = 0; k < 6; k++)
        {
            document.getElementById("categoryButton"+k).innerHTML = self.categoryList[k].title;
        }
        
        // populate values
        for (var i = 0; i < 6; i++)
        {
            for (var j = 0; j < 5; j++)
            {
                document.getElementById("valueC" + i + "Q" + j).innerHTML = "$"+self.categoryList[i].questionsList[j].value;
            }
        }
    },
    
    
    getCategoryTitles: function()
    {
        var self = this;
        
        for (var i = 0; i < self.categoryList.length; i++)
        {
            self.categoryTitleList.push(self.categoryList[i].title);
        }
        
        return self.categoryTitleList;
    },
    
    
    // disable all category buttons
    disableCategoryButtons: function()
    {
        // first 5 categories in list are the dynamic categories
        for (var i = 0; i < 6; i++)
        {
            document.getElementById("categoryButton"+i).disabled = true;
        }
    },
    
    // enable available category buttons
    enableCategoryButtons: function()
    {
        var self = this;
        
        // first 5 categories in list are the dynamic categories
        for (var i = 0; i < 6; i++)
        {
            if (self.categoryList[i].isCategoryAvailable())
            {
                document.getElementById("categoryButton"+i).disabled = false;
            }
        }
    }
}



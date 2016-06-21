




module.exports = {
    "env": {
        "node": true
    },
    "parserOptions": {
      "ecmaVersion": 6  
    },
    "rules": {
        "callback-return": "warn",
		"global-require": "warn",
		"handle-callback-err": "error",
		"no-mixed-requires": "error",
		"no-new-require": "error",
		"no-catch-shadow": "error",
        "camelcase": "warn",
        "indent": [
            "warn",
            4
        ],
        "linebreak-style": [
            "warn",
            "windows"
        ],
        "quotes": [
            "warn",
            "double"
        ],
        "semi": [
            "error",
            "always"
        ],
		"comma-style": [
            "error",
             "last"
        ],
		"comma-spacing": [
            "error", 
            { 
                "before": false, 
                "after": true 
            }
        ],
		"array-bracket-spacing": [
            "error", 
            "always"
        ],
		"func-style": [
            "warn", 
            "expression"
        ],
		"max-depth": [
            "error", 
            3
        ],
		"max-len": [
            "error", 
            80, 
            4
        ]
    }
};
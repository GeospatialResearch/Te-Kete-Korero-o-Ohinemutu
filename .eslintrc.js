module.exports = {
  root: true,
  // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
  extends: [
    'plugin:vue/recommended',        // /base, /essential, /strongly-recommended, /recommended
    'eslint:recommended'
  ],
  parserOptions: {
    "parser": "babel-eslint",
    "ecmaVersion": 2017,
    "sourceType": "module"
  },
  // required to lint *.vue files
  plugins: [
    'eslint-plugin-html',
    'eslint-plugin-vue'
  ],
  // add your custom rules here
  rules: {
    // allow mixed/messy quotes
    'quotes': 0,
    // allow paren-less arrow functions
    'arrow-parens': 0,
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
    // we have code that has underscores... ignore this
    'camelcase': 0,
    "vue/max-attributes-per-line": "off",
    "no-console": "off"
  },
  globals: {
    "API_HOST": true,
    "$": true,
    "localStorage": true,
    "FormData": true,
    "Blob": true
  },
  env: {
    // "browser": true,
    // "amd": true,
    "node": true
  }
}

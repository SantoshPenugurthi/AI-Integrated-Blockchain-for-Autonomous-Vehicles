const MyContract = artifacts.require("SmartContract");

module.exports = function(deployer) {
  deployer.deploy(MyContract);
};
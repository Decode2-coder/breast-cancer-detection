const PatientConsent = artifacts.require("PatientConsent");

module.exports = function (deployer) {
  // Deploy the PatientConsent contract
  deployer.deploy(PatientConsent);
};

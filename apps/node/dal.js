// in a production system, we recommend using a datastore
const data = {};

const getState = (key) => {
  return data[key];
};

const setState = (key, value) => {
  data[key] = value;
};

exports.getState = getState;
exports.setState = setState;

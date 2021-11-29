data = {};

const getState = () => {
  return data;
};

const setState = (key, value) => {
  data[key] = value;
};

exports.getState = getState;
exports.setState = setState;
